import streamlit as st
import matplotlib.pyplot as plt
from core.plot_logger import MatplotlibPlotLogger

def render_nasa_integrated_cockpit():
    # ... Pre-existing slider and data processing math ...
    
    # Initialize your new documentation file logger module
    plot_logger = MatplotlibPlotLogger()
    
    # Create the figure drawing canvas mapping the cross-corporate mesh...
    fig, ax = plt.subplots(figsize=(10, 4.5))
    
    # ... (Matplotlib configuration code from your previous prompt) ...
    
    st.pyplot(fig)
    
    # Automatically log a tracking image capture if requested by your operators
    if st.button("📸 Capture & Save Engineering Geometry Snapshot"):
        saved_img_path = plot_logger.log_figure_to_docs(fig, phase_name="Live_Assembly")
        st.success(f"💾 Geometry snapshot compiled securely to: `{saved_img_path}`")
