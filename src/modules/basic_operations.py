import copy

import streamlit as st

from src.core.signals import get_available_signals, get_signal_modes
from src.ui.build_signals import build_signal_ui
from src.ui.plots import plot_signal
from src.utils.time_axis import TimeAxis


def run_basic_operations_module():
    # Mode Selection
    # --------------------------------
    signal_mode = st.radio(
        "Signal Mode",
        get_signal_modes(),
        index=0,
        horizontal=True,
    )

    col0, col1, col2, col3 = st.columns(4)

    with col0:
        signal_type = st.selectbox("Select Signal", get_available_signals())

    with col1:
        t_min = st.number_input("Start Time", value=-5.0, step=0.1, format="%.5f")

    with col2:
        t_max = st.number_input("End Time", value=5.0, step=0.1, format="%.5f")

    with col3:
        fs = st.number_input(
            "Sampling Frequency (Hz)",
            min_value=1,
            max_value=50000,
            value=1000,
            step=100,
            help="Too high frequency may crash the app",
        )

    if t_min >= t_max:
        st.warning("Start time must be less than end time.")
        return

    # Time Axis Generation
    # --------------------------------
    time = TimeAxis(t_min=t_min, t_max=t_max, dt=1 / fs, signal_mode=signal_mode)
    t = time.generate()

    # Signal Construction
    # --------------------------------
    signal = build_signal_ui(signal_type)

    st.markdown("-----")
    st.markdown("#### Basic Transformations")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    with col_s1:
        shift_time = st.number_input("Time Shift (τ)", value=0.0, step=0.1)
    with col_s2:
        time_scale_factor = st.number_input(
            "Time Scaling (a)", value=1.0, step=0.1, min_value=float(0.0)
        )
    with col_s3:
        fold_signal = st.checkbox("Time Inversion (-t)", value=False)

    # Apply Transformations
    # ------------------------------
    transformed_signal = copy.deepcopy(signal)

    if fold_signal:
        transformed_signal = transformed_signal.fold()

    if time_scale_factor != 1.0:
        transformed_signal = transformed_signal.time_scale(time_scale_factor)

    if shift_time != 0.0:
        transformed_signal = transformed_signal.time_shift(shift_time)

    # Output
    # --------------------------------
    st.markdown("-----")
    y_original = signal.evaluate(t)
    y_transformed = transformed_signal.evaluate(t)
    col_left, _, col_right = st.columns([1, 0.1, 1])

    # Left column: Input Signal
    # ------------------------
    with col_left:
        st.text("Input Signal")

        fig = plot_signal(
            t,
            y_original,
            title=f"{signal._base_formula}",
            discrete=True if signal_mode == "Discrete" else False,
            autoscale=True,
        )
        st.plotly_chart(fig, use_container_width=True, key="input_signal")

    # Right column: Output Plot
    # ------------------------
    with col_right:
        st.text("Transformed Signal")

        fig = plot_signal(
            t,
            y_transformed,
            title=f"{transformed_signal.formula}",
            discrete=True if signal_mode == "Discrete" else False,
            autoscale=True,
        )
        st.plotly_chart(fig, use_container_width=True, key="transformed_signal")
