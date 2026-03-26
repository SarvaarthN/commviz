import numpy as np
import streamlit as st

# Project Imports
from src.core.signals import get_available_signals
from src.ui.build_signals import build_signal_ui
from src.ui.plots import plot_signal
from src.utils.time_axis import TimeAxis


def run_energy_power_module():
    st.markdown("## ⚡ Energy & Power of Signals")
    st.text(
        "Understand energy signals, power signals, and why they matter in communication systems"
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

    # Energy & Power Computation
    # -------------------------------------------------
    signal_type, E, P = signal.classify_signal(t)

    # Display Section
    # -------------------------------------------------
    st.markdown("---")
    col_1, col_2, col_3 = st.columns([1, 1, 1])

    with col_1:
        st.metric("Total Energy (E)", f"{E:.6f}")
    with col_2:
        st.metric("Average Power (P)", f"{P:.6f}")
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
        # Sliding window power (for visualization)
        window_size = max(10, int(0.05 * len(x)))  # 5% window
        power_time = np.convolve(
            np.abs(x) ** 2, np.ones(window_size) / window_size, mode="same"
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
