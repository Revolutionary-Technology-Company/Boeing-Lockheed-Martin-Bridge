import streamlit as st
import numpy as np
from ng_tactical.message_generator import Link16MessageGenerator
from ng_tactical.link16_parser import NorthropGrummanLink16Parser

def render_tactical_tracking_dashboard():
    # Instantiate modules inside the dashboard execution loop
    generator = Link16MessageGenerator(baseline_track_id=2048)
    parser = NorthropGrummanLink16Parser()

    st.sidebar.subheader("📡 Northrop Grumman Link 16 Simulator")
    simulate_signal = st.sidebar.checkbox("Engage Live J-Series Telemetry Stream", value=True)
    
    if simulate_signal:
        # 1. Generate live binary message buffer
        raw_bytes = generator.generate_live_j2_packet(base_coordinate=500.0)
        
        # 2. Extract and decode payload properties using the core parser module
        decoded_data = parser.parse_j_series_track_packet(raw_bytes)
        
        # 3. Read tactical variables into dashboard telemetry meters
        st.sidebar.success(f"📟 Track Sync: {decoded_data['link16_label']} | ID: {decoded_data['source_track_id']}")
        
        # Inject the parsed scale factor directly into your Matplotlib airframe line plot math
        tactical_scalar = decoded_data["scaled_displacement_factor"]
    else:
        tactical_scalar = 0.0
