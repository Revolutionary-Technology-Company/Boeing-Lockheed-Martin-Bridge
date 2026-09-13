import streamlit as st
import json
import time

def render_ng_tactical_cockpit_extension():
    st.subheader("📡 Northrop Grumman Link 16 Network Interface")
    
    col_status, col_route = st.columns(2)
    with col_status:
        st.metric("Northrop Grumman Link 16 Node", "tadil_node_ng", delta="SECURE SYNC")
    with col_route:
        st.text("Tactical Routing Boundary:\nhttps://interface.tadil_node_ng.northropgrumman.com")

    # Inbound message postMessage JavaScript broadcast configurations include the NG endpoint
    cad_payload = {"link16_synchronized": True, "timestamp": time.time()}
    iframe_ng_extension_javascript = f"""
    <script>
        const payload = {json.dumps(cad_payload)};
        parent.postMessage({{ type: "LINK16_JSERIES_SYNC", data: payload }}, "https://interface.tadil_node_ng.northropgrumman.com");
    </script>
    """
