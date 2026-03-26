import numpy as np
import streamlit as st

from src.ui.build_signals import build_signal_ui
from src.ui.plots import plot_signal
from src.utils.time_axis import TimeAxis
from src.core.signals import get_available_signals, get_signal_modes


def run_convolution_module():
    st.header("Convolution Operation")
    st.markdown(
        """
        **Definition:** Convolution is a mathematical operation that expresses the output of a system
        in terms of its input signal and impulse response.

        **Continuous-time formula:** $y(t) = \\int_{-\\infty}^{\\infty} x(\\tau) h(t-\\tau) d\\tau$

        **Discrete-time formula:** $y[n] = \\sum_{k=-\\infty}^{\\infty} x[k] h[n-k]$
        """
    )
    st.markdown("----")

    # Time axis inputs
    signal_mode = st.radio("Signal Mode", get_signal_modes(), index=0, horizontal=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        t_min = st.number_input(
            "Start Time", value=0.0, step=0.1, format="%.5f", key="conv_t_min"
        )
    with c2:
        t_max = st.number_input(
            "End Time", value=1.0, step=0.1, format="%.5f", key="conv_t_max"
        )
    with c3:
        fs = st.number_input(
            "Sampling Frequency (Hz)",
            min_value=10,
            max_value=50000,
            value=1000,
            step=100,
            key="conv_fs",
        )

    if t_min >= t_max:
        st.warning("Start time must be less than end time.")
        return

    # Generate time axis
    time = TimeAxis(t_min=t_min, t_max=t_max, dt=1.0 / fs, signal_mode=signal_mode)
    t = time.generate()

    # Two input signals side-by-side
    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("### Input Signal 1")
        sig1_type = st.selectbox(
            "Select Signal", get_available_signals(), key="conv_sig1_type"
        )
        sig1 = build_signal_ui(sig1_type, key_prefix="conv_sig1")

        st.markdown("**Transformations**")
        tau1 = st.number_input(
            "Time Shift (τ)", value=0.0, step=0.1, key="conv_sig1_tau"
        )
        a1 = st.number_input("Time Scale (a)", value=1.0, step=0.1, key="conv_sig1_a")
        amp1 = st.slider("Amplitude Scale", -5.0, 5.0, 1.0, 0.1, key="conv_sig1_amp")
        fold1 = st.checkbox("Time Inversion (-t)", value=False, key="conv_sig1_fold")

        # Apply transforms
        if tau1 != 0.0:
            sig1 = sig1.time_shift(tau1)
        if a1 != 1.0:
            sig1 = sig1.time_scale(a1)
        if fold1:
            sig1 = sig1.fold()
        if amp1 != 1.0:
            sig1 = sig1 * amp1

    with right_col:
        st.markdown("### Input Signal 2")
        sig2_type = st.selectbox(
            "Select Signal", get_available_signals(), key="conv_sig2_type"
        )
        sig2 = build_signal_ui(sig2_type, key_prefix="conv_sig2")

        st.markdown("**Transformations**")
        tau2 = st.number_input(
            "Time Shift (τ)", value=0.0, step=0.1, key="conv_sig2_tau"
        )
        a2 = st.number_input("Time Scale (a)", value=1.0, step=0.1, key="conv_sig2_a")
        amp2 = st.slider("Amplitude Scale", -5.0, 5.0, 1.0, 0.1, key="conv_sig2_amp")
        fold2 = st.checkbox("Time Inversion (-t)", value=False, key="conv_sig2_fold")

        # Apply transforms
        if tau2 != 0.0:
            sig2 = sig2.time_shift(tau2)
        if a2 != 1.0:
            sig2 = sig2.time_scale(a2)
        if fold2:
            sig2 = sig2.fold()
        if amp2 != 1.0:
            sig2 = sig2 * amp2

    # Evaluate signals
    x = sig1.evaluate(t)
    h = sig2.evaluate(t)

    # Plot inputs
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**Signal 1:** {sig1.formula}")
        st.plotly_chart(
            plot_signal(t, x, title=sig1.formula, discrete=(signal_mode == "Discrete")),
            use_container_width=True,
            key="conv_sig1_plot",
        )
    with col_b:
        st.markdown(f"**Signal 2:** {sig2.formula}")
        st.plotly_chart(
            plot_signal(t, h, title=sig2.formula, discrete=(signal_mode == "Discrete")),
            use_container_width=True,
            key="conv_sig2_plot",
        )

    st.markdown("----")

    # Convolution mode
    conv_mode = st.selectbox(
        "Convolution Mode", ["full", "same", "valid"], index=0, key="conv_mode_select"
    )

    # Compute convolution (use full then slice t accordingly to keep time alignment correct)
    dt = t[1] - t[0] if len(t) > 1 else 1.0
    y_full = np.convolve(x, h, mode="full") * dt
    full_len = y_full.size
    t_full = np.linspace(2 * t[0], 2 * t[-1], full_len)

    if conv_mode == "full":
        y = y_full
        t_out = t_full
    else:
        y = np.convolve(x, h, mode=conv_mode) * dt
        n_y = len(y)
        start = (full_len - n_y) // 2
        t_out = t_full[start : start + n_y]

    # Output plot
    st.markdown("### Output Signal (Convolution Result)")
    st.plotly_chart(
        plot_signal(
            t_out, y, title=f"y(t) = {sig1.formula} * {sig2.formula}", discrete=False
        ),
        use_container_width=True,
        key="conv_output_plot",
    )
