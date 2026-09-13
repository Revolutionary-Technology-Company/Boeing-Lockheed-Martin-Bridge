import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from core.active_multimuxer import ActiveBridgeMultimuxer

def render_multimuxer_bridge_panel():
    st.subheader("🎚️ Active Multimuxer / Demultimuxer Matrix")
    st.caption("Consolidates multi-corporate circuit logic into a single channel [No Code Buffers]")

    # Initialize multiplexer
    mux_core = ActiveBridgeMultimuxer()

    st.sidebar.header("🔌 Multimuxer Signal Routing")
    active_corporate_channels = st.sidebar.slider("Active Enterprise Node Feeds Input", 2, 6, 6)
    signal_load = st.sidebar.slider("Base Input Signal Value", 10.0, 300.0, 150.0)

    # Compile mock concurrent channel tracks (Boeing, Lockheed, etc.)
    mock_channels = np.random.uniform(signal_load - 10, signal_load + 10, (100, active_corporate_channels))

    # Compress streams down to a single signal via multi-core parallel routines
    mux_payload = mux_core.multiplex_corporate_inputs(mock_channels)

    # Present Metrics
    col_buffers, col_hex, col_status = st.columns(3)
    with col_buffers:
        st.metric("Individual Code Buffers Replaced", mux_payload["active_code_buffers_replaced"], delta="-100% Overhead")
    with col_hex:
        st.metric("Mux Single Signal Potential", mux_payload["hex_voltage_state"])
    with col_status:
        st.success("⚡ Single Signal Multiplex Active")

    # Plot single signal conversion stream via Matplotlib
    st.write("### 📊 Consolidated Transmission Waveform (Bypassing Buffers)")
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.set_facecolor('#111')
    fig.patch.set_facecolor('#111')
    
    ax.plot(mux_payload["multiplexed_signal_vector"], color='#00ffcc', linewidth=2, label="Single Compressed Output Signal Stream")
    ax.grid(True, color='#222')
    ax.tick_params(colors='white')
    ax.set_ylabel("Signal Amplitude", color='white')
    ax.legend(facecolor='#1a1a1a', edgecolor='#333').get_texts().set_color('white')
    st.pyplot(fig)
