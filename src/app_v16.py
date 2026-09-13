import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
from core.bridge_gravity_induction import BridgeGravityInductionEngine

def render_bridge_gravity_panel():
    st.subheader("Boeing-Lockheed Martin Bridge Gravity Induction Core")
    st.caption("Shared Project Network Environmental Calibration Grid [Audited Node]")
    
    # Initialize engine block
    gravity_core = BridgeGravityInductionEngine(target_gravity_g=1.0)
    
    # 1. Dashboard Controls
    st.sidebar.subheader("Bridge Plate Polarization Matrix")
    ceiling_charge = st.sidebar.slider("Ceiling Structural Electron Charge (C)", 0.0, 60.0, 45.0, step=0.5)
    floor_ground = st.sidebar.slider("Floor Negative Ground Potential (C)", -60.0, 0.0, -45.0, step=0.5)
    
    # 2. Process Telemetry Through Core Logic
    telemetry = gravity_core.calculate_bridge_field_differential(ceiling_charge, floor_ground)
    
    # 3. Present Metric Indicators
    col_g, col_hex, col_status = st.columns(3)
    with col_g:
        st.metric("Bridge Induced Gravity Vector", f"{telemetry['induced_g_force_magnitude']:.2f} G")
    with col_hex:
        st.metric("Hex Matrix Signal Output", telemetry["hex_voltage_state"])
    with col_status:
        if telemetry["bridge_field_status"] == "NOMINAL_STABLE":
            st.success("Induction Matrix Stable")
        elif telemetry["bridge_field_status"] == "DEGRADED_GRAVITY_FIELD":
            st.warning("Low Differential Field")
        else:
            st.error("CRITICAL SHIELD SHORT-CIRCUIT!")

    # 4. Plot Field Distribution Cross-Sections via Matplotlib
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.set_facecolor('#111')
    fig.patch.set_facecolor('#111')
    
    z_axis = np.linspace(-5, 5, 100)
    field_potential = np.linspace(ceiling_charge, floor_ground, 100)
    
    ax.plot(z_axis, field_potential, color='#00ffcc', linewidth=2, label="Magnetic Electron Force Vector Profile")
    ax.fill_between(z_axis, ceiling_charge, field_potential, color='#00ffcc', alpha=0.05)
    
    ax.grid(True, color='#222')
    ax.tick_params(colors='white')
    ax.set_ylabel("Bridge Plate Potential (Coulombs)", color='white')
    ax.legend(facecolor='#1a1a1a', edgecolor='#333').get_texts().set_color('white')
    st.pyplot(fig)

    # 5. Broadcast Secure Sync Vectors to Multi-Corporate Domain Endpoints
    cad_payload = {"induced_g": telemetry["induced_g_force_magnitude"], "status": telemetry["bridge_field_status"]}
    st.components.v1.html(f"""
    <script>
        const payload = {json.dumps(cad_payload)};
        // Broadcasts safely to both corporate endpoints via postMessage channels
        parent.postMessage({{ type: "BRIDGE_GRAVITY_SYNC", data: payload }}, "https://boeing.com");
        parent.postMessage({{ type: "BRIDGE_GRAVITY_SYNC", data: payload }}, "https://interface.01_node_://lockheedmartin.com");
    </script>
    """, height=0)
