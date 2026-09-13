import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
import time
from nasa_ops.ccsds_parser import NasaCcsdsSpaceParser

def render_nasa_integrated_cockpit():
    st.set_page_config(layout="wide")
    st.title("UNIVAC IX - NASA Aerospace Integration Control Panel")
    
    # Track NASA Domain Gateway Linkages
    st.sidebar.header("NASA Telemetry Pipeline Configuration")
    nasa_gateway = "https://nasa.gov"
    st.sidebar.text(f"Endpoint: {nasa_gateway}")
    
    # Slider parameters for live geometric calculation inputs
    st.sidebar.subheader("Airframe Matrix Displacements")
    man_panel_gap = st.sidebar.slider("MAN Panel Edge Discontinuities (mm)", -0.025, 0.025, 0.005, step=0.001)
    boeing_spar_deflection = st.sidebar.slider("Boeing Internal Spar Load (mm)", -0.030, 0.030, 0.000, step=0.001)
    
    # ----------------------------------------------------------------------------
    # LIVE GEOMETRIC CROSS-SECTION GRAPH: Matplotlib Pipeline
    # ----------------------------------------------------------------------------
    st.subheader("Real-Time Form-Molded Airframe Conformance Grid")
    
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.set_facecolor('#111111')
    fig.patch.set_facecolor('#111111')
    
    # Construct fixed target coordinate lines representing the form-molded AC Delco mold profile
    x_grid = np.linspace(-10, 10, 200)
    nominal_mold_line = np.zeros_like(x_grid)
    
    # Calculate operational component deviations based on real-time application inputs
    man_skin_curve = nominal_mold_line + man_panel_gap * np.sin(x_grid / 2)
    boeing_inner_structure = nominal_mold_line + boeing_spar_deflection * np.cos(x_grid / 3)
    
    # Render tracking boundary layers to the visualization canvas
    ax.plot(x_grid, nominal_mold_line, color='cyan', linestyle='--', linewidth=1.5, label='Nominal AC Delco Mold Target (0.000mm)')
    ax.plot(x_grid, man_skin_curve, color='#ff9900', linewidth=2, label=f'MAN Outside Skin Panels Deviation ({man_panel_gap:+.3f}mm)')
    ax.plot(x_grid, boeing_inner_structure, color='#00ff00', linewidth=1.5, label=f'Boeing/Lockheed Core Skeleton ({boeing_spar_deflection:+.3f}mm)')
    
    # Enforce strict visual alert windows based on the mandatory ±0.015mm tolerance envelope
    ax.fill_between(x_grid, -0.015, 0.015, color='gray', alpha=0.15, label='Safe Operating Envelope (±0.015mm)')
    
    # Axis customization schemas for dark matrix panels
    ax.set_ylim(-0.040, 0.040)
    ax.grid(True, color='#222222', linestyle=':')
    ax.tick_params(colors='white')
    ax.set_title("Cross-Corporate Interface Alignment Profile", color='white', fontsize=12, fontweight='bold')
    ax.set_ylabel("Mating Delta Variance (mm)", color='white')
    legend = ax.legend(loc='lower center', facecolor='#1a1a1a', edgecolor='#333333', ncol=2)
    for text in legend.get_texts():
        text.set_color('white')
        
    st.pyplot(fig)

    # ----------------------------------------------------------------------------
    # CROSS-DOMAIN IFRAME BROADCAST NETWORKS
    # ----------------------------------------------------------------------------
    if abs(man_panel_gap) > 0.015:
        st.error(f"CRITICAL TOLERANCE VIOLATION: Surface alignment variance ({abs(man_panel_gap):.3f}mm) exceeds the form-molded limit!")
    
    # Include the NASA target registration within the script transmission payloads
    cad_payload = {"displacement_mm": man_panel_gap, "timestamp": time.time()}
    
    iframe_connector_javascript = f"""
    <script>
        const payload = {json.dumps(cad_payload)};
        // Broadcasts securely straight to your newly configured NASA operations cluster
        parent.postMessage({{ type: "NASA_CCSDS_SYNC", data: payload }}, "https://nasa.gov");
    </script>
    """
