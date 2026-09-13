import streamlit as st
import json
import time
from man_powertrain.j1939_parser import ManSurfacePanelsParser

def render_aerospace_surface_cockpit():
    st.subheader("External Skin & Panel Tolerances (MAN Aerodynamic Engineering)")
    
    # Instantiate surface telemetry loop
    surface_parser = ManSurfacePanelsParser()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("MAN External Panel Feed", "fleet_://man.com", delta="FLUSH SURFACE")
    with col2:
        panel_gap = st.slider("MAN Panel Edge Mating Clearance (mm)", 0.005, 0.030, 0.012, step=0.001)
    with col3:
        st.metric("Geometric Structural Status", "CONFORMANT" if panel_gap <= 0.015 else "CRITICAL SKEW")

    # If the external surface panel gap exceeds your strict ±0.015mm form-molded envelope, trip the auditor
    if panel_gap > 0.015:
        st.error("CRITICAL SURFACE MISALIGNMENT: MAN Exterior Panel exceeds airframe mating tolerances!")
        # Triggers your LiveAssemblyAuditor action selection automatically...
