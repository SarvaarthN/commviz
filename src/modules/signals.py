import numpy as np
import streamlit as st

# Project Imports
from src.core.signals import get_available_signals, get_signal_modes
from src.ui.build_signals import build_signal_ui
from src.ui.plots import plot_signal
from src.utils.time_axis import TimeAxis


def run_signals_module():

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

    # Evaluation
    # --------------------------------
    y = signal.evaluate(t)

    st.markdown("-----")

    # Output
    # --------------------------------
    col_left, _, col_right = st.columns([1, 0.2, 4])

    # Left column: axis limits
    # ------------------------
    with col_left:
        st.text("Axis Limits")

        # Row 1: X-axis limits
        x1, x2 = st.columns(2)
        with x1:
            x_min = st.number_input("X min", value=float(t[0]), step=0.1)
        with x2:
            x_max = st.number_input("X max", value=float(t[-1]), step=0.1)

        # Row 2: Y-axis limits
        y1, y2 = st.columns(2)
        with y1:
            y_min = st.number_input("Y min", value=float(np.min(y)), step=0.1)
        with y2:
            y_max = st.number_input("Y max", value=float(np.max(y)), step=0.1)

        # Sanity check
        if x_min >= x_max:
            st.warning("X min must be less than max. Using auto-scale.")
            x_range = None
        else:
            x_range = (x_min, x_max)

        if y_min >= y_max:
            st.warning("Y min must be less than max. Using auto-scale.")
            y_range = None
        else:
            y_range = (y_min, y_max)

        st.text("Other Parameters")

        p1, p2 = st.columns(2)
        with p1:
            enable_zero_line = st.checkbox("Zero Line", value=False, help=None)
        with p2:
            show_grid = st.checkbox("Show Grid", value=True, help=None)

    # Right column: Signal Plot
    # ------------------------
    with col_right:
        fig = plot_signal(
            t,
            y,
            title=f"{signal.formula}",
            discrete=True if signal_mode == "Discrete" else False,
            xlim=x_range,
            ylim=y_range,
            autoscale=False,
            enable_zero_line=enable_zero_line,
            show_grid=show_grid,
        )
        st.plotly_chart(fig, use_container_width=True)
