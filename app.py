import streamlit as st

from src.modules.basic_operations import run_basic_operations_module
from src.modules.energy_power_signals import run_energy_power_module
from src.modules.signals import run_signals_module
from src.modules.convolution import run_convolution_module

st.set_page_config(layout="wide", page_title="CS Viz", menu_items={})

# Reduce top padding of the main container
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 0rem;
    }
    header {
        background-color: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("## Comm. Systems Visualizer")
st.sidebar.markdown("---")

signal_topic = st.sidebar.radio(
    "Signal Analysis",
    [
        "Signal Fundamentals",
        "Basic Signal Operations",
        "Energy and Power Signals",
        "Convolution",
    ],
    key="signal_analysis",
)
digital_comm_topic = st.sidebar.radio(
    "Digital Communication",
    [
        "Sampling Theorem",
    ],
    key="digital_comm",
)

if signal_topic == "Signal Fundamentals":
    run_signals_module()
if signal_topic == "Basic Signal Operations":
    run_basic_operations_module()
if signal_topic == "Energy and Power Signals":
    run_energy_power_module()
if signal_topic == "Convolution":
    run_convolution_module()
