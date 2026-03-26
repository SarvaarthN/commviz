import numpy as np
import streamlit as st

from src.core.signals import (
    exponential,
    ramp,
    rectangular_pulse,
    signum_signal,
    sinc_signal,
    sinusoid,
    triangular_wave,
    unit_impulse,
    unit_step,
)


def build_signal_ui(signal_type: str, key_prefix: str = ""):
    """
    Reusable UI component for building signals.
    Returns a Signal object.

    key_prefix: optional string to make streamlit widget keys unique when this UI
    is rendered multiple times on the same page (e.g., for two input signals).
    """

    # Unit Impulse
    # -------------------------------
    if signal_type == "Unit Impulse":
        return unit_impulse()

    # Unit Step
    # -------------------------------
    elif signal_type == "Unit Step":
        col1, col2 = st.columns([1, 2])

        with col1:
            constant = st.slider(
                "Amplitude",
                0.1,
                5.0,
                1.0,
                0.1,
                key=f"{key_prefix}_step_amplitude",
            )

        return unit_step(constant)

    # Ramp
    # -------------------------------
    elif signal_type == "Ramp":
        return ramp()

    # Exponential
    # -------------------------------
    elif signal_type == "Exponential":
        col1, col2 = st.columns([1, 1])

        with col1:
            a = st.slider(
                "Exponent (a)", -5.0, 5.0, 1.0, 0.1, key=f"{key_prefix}_expo_a"
            )
        with col2:
            c = st.slider(
                "Constant (a)", -5.0, 5.0, 1.0, 0.1, key=f"{key_prefix}_expo_c"
            )

        return exponential(c, a)

    # Sinusoidal
    # -------------------------------
    elif signal_type == "Sinusoidal":
        col1, col2, col3 = st.columns(3)

        with col1:
            amplitude = st.slider(
                "Amplitude", 0.1, 5.0, 1.0, 0.1, key=f"{key_prefix}_sin_amplitude"
            )

        with col2:
            frequency = st.slider(
                "Frequency (Hz)", 0.1, 10.0, 1.0, 0.1, key=f"{key_prefix}_sin_frequency"
            )

        with col3:
            phase = st.slider(
                "Phase (rad)", -np.pi, np.pi, 0.0, 0.1, key=f"{key_prefix}_sin_phase"
            )

        return sinusoid(amplitude, frequency, phase)

    # Sinc Signal
    # -------------------------------
    elif signal_type == "Sinc":
        col1 = st.columns(1)[0]
        with col1:
            amplitude = st.slider(
                "Amplitude", 0.1, 5.0, 1.0, 0.1, key=f"{key_prefix}_sinc_amplitude"
            )
        return sinc_signal(amplitude)

    # Signum Signal
    # -------------------------------
    elif signal_type == "Signum":
        return signum_signal()

    # Rectangular Pulse
    # -------------------------------
    elif signal_type == "Rectangular":
        col1, col2, col3 = st.columns(3)
        with col1:
            start = st.number_input(
                "Start time", -5.0, 5.0, -1.0, 0.1, key=f"{key_prefix}_rect_start"
            )
        with col2:
            end = st.number_input(
                "End time", -5.0, 5.0, 1.0, 0.1, key=f"{key_prefix}_rect_end"
            )
        with col3:
            amplitude = st.slider(
                "Amplitude", 0.1, 5.0, 1.0, 0.1, key=f"{key_prefix}_rect_amplitude"
            )
        return rectangular_pulse(start, end, amplitude)

    # Triangular Wave
    # -------------------------------
    elif signal_type == "Triangular":
        col1, col2, col3 = st.columns(3)
        with col1:
            start = st.number_input(
                "Start time",
                -5.0,
                5.0,
                -1.0,
                0.1,
                key=f"{key_prefix}_tri_start",
            )
        with col2:
            end = st.number_input(
                "End time",
                -5.0,
                5.0,
                1.0,
                0.1,
                key=f"{key_prefix}_tri_end",
            )
        with col3:
            amplitude = st.slider(
                "Amplitude", 0.1, 5.0, 1.0, 0.1, key=f"{key_prefix}_tri_amplitude"
            )
        return triangular_wave(start, end, amplitude)

    # Fallback (safety)
    # -------------------------------
    else:
        st.error("Unknown signal type")
        return None
