import streamlit as st
import json
import time

def render_industrial_aerospace_cockpit():
    st.subheader("Tri-Corporate Network Gateway Status")
    
    col_lm, col_boeing, col_ab = st.columns(3)
    
    with col_lm:
        st.metric("Lockheed Martin Gateway", "interface.01_node_ca", delta="ACTIVE")
    with col_boeing:
        st.metric("Boeing Commercial Server", "skew.boeing.commercial", delta="ACTIVE")
    with col_ab:
        st.metric("Allen-Bradley Industrial Node", "plc_://allen-bradley.com", delta="ACTIVE", delta_color="normal")

    # Inside the postMessage iframe broadcast array, append the Allen-Bradley distribution endpoint:
    cad_payload = {
        "wingspan_offset": 15000.0,
        "cip_bus_synchronized": True,
        "timestamp": time.time()
    }
    
    cad_javascript_extension = f"""
    <script>
        const payload = {json.dumps(cad_payload)};
        
        function broadcastToAllDomains() {{
            // ... Previous frame bindings for Boeing & Lockheed Martin ...
            
            const abFrame = document.getElementById('allen-bradley-frame');
            if(abFrame && abFrame.contentWindow) {{
                abFrame.contentWindow.postMessage({{ 
                    type: "CAD_MODEL_SYNC", 
                    data: payload 
                }}, "https://interface.plc_matrix.rockwell.allen-bradley.com");
            }}
        }}
    </script>
    """
