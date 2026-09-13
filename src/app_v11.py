import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from core.antigravity_core import ACDelcoAntigravityEngine
from core.eclss_system import ACDelcoEclssManager

def render_antigravity_cockpit():
    st.title("🛸 UNIVAC IX - Antigravity Control Cockpit")
    st.caption("Gundam Robotics Type-S Saiya Chassis Integration Grid")

    # Initialize Core Mechanical Simulation Components
    ag_engine = ACDelcoAntigravityEngine(vessel_mass_kg=1000.0)
    eclss = ACDelcoEclssManager()

    st.sidebar.header("⚡ Charge Routing Profiles")
    active_charge = st.sidebar.slider("Ventral Plate Static Charge (Coulombs)", 0.0, 120.0, 98.0, step=1.0)
    fluid_psi = st.sidebar.slider("ECLSS Fluid Line Pressure (PSI)", 20.0, 60.0, 45.0, step=0.5)

    # 1. Evaluate Core Liftoff Conditions
    hover_threshold = ag_engine.calculate_required_hover_charge()
    hex_state = ag_engine.map_plate_potential_to_hex(active_charge)
    eclss_status = eclss.process_fluid_loops(fluid_psi, o2_level=21.0)

    # 2. Display Dynamic Telemetry Data Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ventral Hex Core State", f"BIAS: 0.{hex_state}V")
    with col2:
        st.metric("Net Repulsion Force", f"{(active_charge * 100.0):,.0f} N", delta=f"{(active_charge - hover_threshold) * 100.0:+.0f} N vs Hover")
    with col3:
        st.metric("ECLSS Mating Enclosure", eclss_status["status"], delta=eclss_status["message"], delta_color="normal" if eclss_status["status"] == "NOMINAL" else "inverse")

    # 3. Render Real-Time Electrostatic Displacement Plots
    st.subheader("📊 Localized Hull Asymmetric Repulsion Grid")
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_facecolor('#111')
    fig.patch.set_facecolor('#111')

    angles = np.linspace(0, 2 * np.pi, 360)
    # Generate interactive repulsion wave forms based on active slider inputs
    charge_density_wave = active_charge * (1.0 + 0.1 * np.sin(angles * 4))
    
    ax.plot(angles, charge_density_wave, color='#00ffcc', linewidth=2, label="Ventral 360-Plate Density Spectrum")
    ax.axhline(hover_threshold, color='red', linestyle='--', label=f"Gravity Balance Line ({hover_threshold} C)")
    ax.fill_between(angles, 0, charge_density_wave, color='#00ffcc', alpha=0.1)
    
    ax.grid(True, color='#222')
    ax.tick_params(colors='white')
    ax.legend(facecolor='#1a1a1a', edgecolor='#333').get_texts()[0].set_color('white')
    st.pyplot(fig)

if __name__ == "__main__":
    render_antigravity_cockpit()
