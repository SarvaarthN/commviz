import numpy as np
import streamlit as st

# Project Imports
from src.core.signals import get_available_signals
from src.ui.build_signals import build_signal_ui
from src.ui.plots import plot_signal
from src.utils.time_axis import TimeAxis


def safe_format(value):
    # Format float values for display, handling edge cases like inf and NaN
    if np.isinf(value):
        return "∞"
    if np.isnan(value):
        return "Undefined"
    return f"{value:.6f}"


def run_energy_power_module():
    st.markdown("## ⚡ Energy & Power of Signals")
    st.text(
        "Understand energy signals, power signals, and why they matter in communication systems"
    )
    st.warning(
        "Energy and Power are computed over a finite time interval and are approximations."
    )

    # Input Section
    # -------------------------------------------------
    col0, col1, col2, col3 = st.columns(4)

    with col0:
        signal_type = st.selectbox("Select Signal", get_available_signals())

    with col1:
        t_min = st.number_input("Start Time", value=-5.0, step=0.1)

    with col2:
        t_max = st.number_input("End Time", value=5.0, step=0.1)

    with col3:
        fs = st.number_input(
            "Sampling Frequency (Hz)",
            min_value=10,
            max_value=50000,
            value=1000,
            step=100,
            help="Higher values increase accuracy but may slow the app",
        )

    if t_min >= t_max:
        st.error("Start time must be less than end time")
        return

    # Time Axis
    # -------------------------------------------------
    time = TimeAxis(t_min=t_min, t_max=t_max, dt=1 / fs)
    t = time.generate()

    # Signal Construction
    # -------------------------------------------------
    signal = build_signal_ui(signal_type)
    x = signal.evaluate(t)

    # Guard against zero signal early to avoid misleading energy/power output
    if np.all(x == 0):
        st.info("Zero Signal detected")
        return

    if np.max(np.abs(x)) > 1e6:
        st.warning("Signal amplitude too large, might cause numerical instability")

    if len(t) > 1_000_000:
        st.warning("Too many samples may lead to performance issues")

    # Nyquist-based aliasing check — sampling should be at least 10x the signal's max frequency
    if hasattr(signal, "max_frequency"):
        if fs < 10 * signal.max_frequency():
            st.warning("Sampling frequency may be too low and lead to aliasing")

    # Sample interval derived from time axis, used for numerical integration
    dt = t[1] - t[0]

    # Trapezoidal cumulative integral — O(n), equivalent to trapz for uniform dt
    energy_density = np.abs(x) ** 2
    cumulative_energy = np.concatenate(
        [[0], np.cumsum((energy_density[:-1] + energy_density[1:]) / 2 * dt)]
    )

    # Power convergence over symmetric intervals [-T, T] around t=0
    # 300 points is sufficient for a smooth convergence curve
    T_values = np.linspace(0.01, max(abs(t_min), abs(t_max)), 300)
    power_vs_T = np.zeros_like(T_values)

    # Subsample t and x for performance before the convergence loop
    t_loop, x_loop = t, x
    if len(t) > 100_000:
        step = len(t) // 100_000
        t_loop = t[::step]
        x_loop = x[::step]

    for i, T in enumerate(T_values):
        # Create a symmetric mask around t=0
        mask = (t_loop >= -T) & (t_loop <= T)
        if mask.sum() < 2:
            continue
        # Integrate |x(t)|^2 over [-T, T] and normalize by 2T — matches the power formula
        power_vs_T[i] = np.trapz(np.abs(x_loop[mask]) ** 2, t_loop[mask]) / (2 * T)

    # Energy & Power Computation
    # -------------------------------------------------
    # Unpack classification result
    signal_type, E, P = signal.classify_signal(t)

    # Display Section
    # -------------------------------------------------
    st.markdown("---")
    col_1, col_2, col_3 = st.columns([1, 1, 1])

    with col_1:
        st.metric("Total Energy (E)", safe_format(E))
    with col_2:
        st.metric("Average Power (P)", safe_format(P))
    with col_3:
        st.info(signal_type)

    col_left, _, col_right = st.columns([1, 0.1, 1])

    with col_left:
        # Original signal
        fig1 = plot_signal(
            t,
            x,
            title=f"{signal.formula}",
            discrete=False,
            autoscale=True,
        )
        st.plotly_chart(fig1, width="stretch", key="energy_power_signal")

    with col_right:
        # Use a short sliding window to estimate instantaneous power for visualization
        window_time = 0.1  # seconds
        window_size = max(10, int(window_time * fs))  # ensure at least 10 samples

        # Convolve with a box filter to get average power in each window
        power_time = (
            np.convolve(np.abs(x) ** 2, np.ones(window_size), mode="same") / window_size
        )

        # Power over time
        fig2 = plot_signal(
            t,
            power_time,
            title="|x(t)|² (Sliding Window Power)",
            discrete=False,
            autoscale=True,
        )
        st.plotly_chart(fig2, width="stretch", key="energy_power_plot")

    st.subheader("Signal Diagnostics")
    col3, col4 = st.columns(2)

    with col3:
        fig3 = plot_signal(
            t,
            cumulative_energy,
            title="Cumulative Energy",
            discrete=False,
            autoscale=True,
        )
        st.plotly_chart(fig3, width="stretch", key="cumulative_energy_plot")

    with col4:
        # x-axis is T (window half-width), y-axis is power — shows convergence to P
        fig4 = plot_signal(
            T_values,
            power_vs_T,
            title="Power Convergence (symmetric around t=0)",
            discrete=False,
            autoscale=True,
        )
        st.plotly_chart(fig4, width="stretch", key="power_convergence_plot")

    # Educational Notes
    # -------------------------------------------------
    st.markdown("---")
    st.markdown(
        r"""
    ### Energy
    $$
    E = \int_{-\infty}^{\infty} |x(t)|^2 \, dt
    $$

    ### Power
    $$
    P = \lim_{T \to \infty} \frac{1}{2T} \int_{-T}^{T} |x(t)|^2 \, dt
    $$

    ### Interpretation
    - **Energy signals:** finite energy, zero power
    - **Power signals:** infinite energy, finite power
    - **Neither:** infinite energy and infinite power
    """
    )
    st.markdown("### Why This Matters in Communication?")
    st.markdown(
        """
        - **Energy signals** model pulses, packets, and digital symbols
        - **Power signals** model carriers, oscillators, and continuous transmissions
        - Determines:
            - Transmission feasibility
            - Amplifier design
            - Noise analysis
            - Fourier transform applicability
            - Modulation strategies

        This distinction is fundamental in **communication theory, DSP, and information theory**.
        """
    )
