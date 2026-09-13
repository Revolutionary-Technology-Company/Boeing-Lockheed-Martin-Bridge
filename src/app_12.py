import streamlit as st
import matplotlib.pyplot as plt
from core.bak_flight_controller import SaiyaFlightController

def render_advanced_flight_cockpit():
    st.subheader("🕹️ Hypersonic Trajectory Core (Charge Translation Engine)")
    
    # Instantiate flight processing core
    controller = SaiyaFlightController(target_hover_charge=98.0)
    
    col_input, col_graph = st.columns(2)
    with col_input:
        target_angle = st.slider("Trajectory Heading Intercept (Degrees)", 0, 359, 90)
        maneuver_force = st.slider("Asymmetric Delta Bias Intensity", 0.0, 1.5, 0.5)
        
        # Compile active plate density array matrices
        active_plates = controller.compute_steering_matrix(target_angle, maneuver_force)
        st.info(f"📊 Plate Vector Delta Compiled. Max Sector Concentration: {max(active_plates):.4f} C")
        
    with col_graph:
        # Plot full polar distribution profile matching the 360-degree array
        fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})
        ax.set_facecolor('#111')
        fig.patch.set_facecolor('#111')
        
        theta = np.linspace(0, 2*np.pi, 360)
        ax.plot(theta, active_plates, color='#00ffcc', linewidth=2)
        ax.fill(theta, active_plates, color='#00ffcc', alpha=0.2)
        
        ax.grid(True, color='#333')
        ax.tick_params(colors='white')
        st.pyplot(fig)
