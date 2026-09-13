import streamlit as st
import numpy as np
from core.fire_cuda_engine import FireWatchHardwareEngine

def render_firewatch_hardware_cockpit():
    st.subheader("FireWatch Dual-Hardware Acceleration Dashboard")
    st.caption("Synchronized Cross-Corporate Engineering Interface Layer")

    # Initialize the dual-mode processing module
    hardware_core = FireWatchHardwareEngine(target_threshold=180.0)

    st.sidebar.header("Telemetry Controls")
    grid_size = st.sidebar.slider("Matrix Core Sizing (Grid)", 32, 256, 128)
    force_fallback = st.sidebar.checkbox("Force Fallback Multi-Core CPU Routine", value=False)
    trip_fault = st.sidebar.checkbox("Inject Critical Structural Surge Parameters", value=False)

    # Build local 2D matrix arrays
    if trip_fault:
        mock_data = np.full((grid_size, grid_size), 220.0, dtype=np.float32)
    else:
        mock_data = np.random.uniform(15.0, 50.0, (grid_size, grid_size)).astype(np.float32)

    # Execute acceleration testing routines across multi-core systems
    with st.spinner("Processing structural telemetry blocks across hardware tracks..."):
        telemetry = hardware_core.process_matrix_frame(mock_data, force_cpu=force_fallback)

    # Present Active Hardware Telemetry Metrics
    col_engine, col_status, col_hex = st.columns(3)
    with col_engine:
        st.metric("Active Execution Fabric", telemetry["active_hardware_engine"])
    with col_status:
        if telemetry["incident_verification"] == "CRITICAL_THERMAL_SURGE":
            st.error("INCIDENT: THERMAL BREACH DETECTED!")
        else:
            st.success("Structural State Nominal")
    with col_hex:
        st.metric("Hex Matrix Signal Output", telemetry["hex_voltage_state"])
