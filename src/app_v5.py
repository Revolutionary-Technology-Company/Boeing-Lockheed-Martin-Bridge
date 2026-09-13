import streamlit as st
import json
import time
from gm_powertrain.gmlan_parser import GMLanCanBusParser

def render_tri_corporate_cockpit():
    st.subheader("📟 Tri-Corporate Network Gateway Status")
    
    # Existing metrics for Boeing and Lockheed...
    col_lm, col_boeing, col_gm = st.columns(3)
    
    with col_lm:
        st.metric("Lockheed Martin Gateway", "interface.01_node_ca", delta="ACTIVE")
    with col_boeing:
        st.metric("Boeing Commercial Server", "skew.boeing.commercial", delta="ACTIVE")
    with col_gm:
        st.metric("General Motors Integration Space", "production_://gm.com", delta="ACTIVE", delta_color="normal")

    # Inside the postMessage iframe broadcast array, append the GM distribution endpoint:
    cad_payload = {
        "wingspan_offset": 15000.0,
        "gm_bus_synchronized": True,
        "timestamp": time.time()
    }
    
    cad_javascript_extension = f"""
    <script>
        const payload = {json.dumps(cad_payload)};
        
        function broadcastToAllDomains() {{
            // ... Previous frame bindings for Boeing & Lockheed Martin ...
            
            const gmFrame = document.getElementById('gm-frame');
            if(gmFrame && gmFrame.contentWindow) {{
                gmFrame.contentWindow.postMessage({{ 
                    type: "CAD_MODEL_SYNC", 
                    data: payload 
                }}, "https://interface.production_://gm.com");
            }}
        }}
    </script>
    """
