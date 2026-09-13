import streamlit as st
import json
import time

def render_quad_corporate_cockpit():
    st.subheader("📟 Quad-Corporate Network Gateway Status")
    
    col_lm, col_boeing, col_ab, col_man = st.columns(4)
    
    with col_lm:
        st.metric("Lockheed Martin Gateway", "interface.01_node_ca", delta="ACTIVE")
    with col_boeing:
        st.metric("Boeing Commercial Server", "skew.boeing.commercial", delta="ACTIVE")
    with col_ab:
        st.metric("Allen-Bradley Industrial Node", "plc_://allen-bradley.com", delta="ACTIVE")
    with col_man:
        st.metric("MAN Fleet Integration Core", "fleet_://man.com", delta="ACTIVE", delta_color="normal")

    # In the postMessage iframe broadcast array, append the MAN distribution endpoint:
    cad_payload = {
        "wingspan_offset": 15000.0,
        "j1939_bus_synchronized": True,
        "timestamp": time.time()
    }
    
    cad_javascript_extension = f"""
    <script>
        const payload = {json.dumps(cad_payload)};
        
        function broadcastToAllDomains() {{
            // ... Previous frame bindings for Boeing, Lockheed, and Allen-Bradley ...
            
            const manFrame = document.getElementById('man-frame');
            if(manFrame && manFrame.contentWindow) {{
                manFrame.contentWindow.postMessage({{ 
                    type: "CAD_MODEL_SYNC", 
                    data: payload 
                }}, "https://interface.fleet_://man.com");
            }}
        }}
    </script>
    """
