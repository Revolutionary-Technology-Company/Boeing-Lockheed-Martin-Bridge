import streamlit as st
import streamlit.components.v1 as components
import json
import time
from joint_assembly.auditor import LiveAssemblyAuditor
from core.gasket_telemetry import ACDelcoGasketMonitor

def render_aerospace_cockpit():
    st.set_page_config(layout="wide", page_title="UNIVAC IX - Domain Integration Node")
    st.title("✈️ UNIVAC IX Domain Integration Node")
    
    # Initialize Core Simulation Modules
    auditor = LiveAssemblyAuditor()
    gasket_monitor = ACDelcoGasketMonitor(target_pressure=45.0)
    
    # 1. Hardware Control Sidebar
    st.sidebar.header("🛠️ Infrastructure Settings")
    selected_profile = st.sidebar.selectbox("Auditor Emergency Action Profile", list(auditor.action_profiles.keys()))
    
    # Telemetry simulation inputs
    simulated_pressure = st.sidebar.slider("Simulated Gasket Pressure (PSI)", 20.0, 60.0, 45.0, step=0.5)
    wing_span = st.sidebar.slider("Wing Component Scaling Offset (mm)", 12000.0, 18000.0, 15000.0, step=0.5)
    
    # 2. Evaluate Health and Security Actions
    seal_health = gasket_monitor.verify_seal_integrity(simulated_pressure)
    security_action = auditor.process_hazard_mitigation(seal_health["status"], selected_profile)
    
    # Display Domain Network Status
    col_lockheed, col_boeing = st.columns(2)
    with col_lockheed:
        st.metric("Lockheed Martin Node Gateway", "interface.01_node_ca", delta="ACTIVE" if seal_health["status"] == "NOMINAL" else "HALTED", delta_color="normal" if seal_health["status"] == "NOMINAL" else "inverse")
    with col_boeing:
        st.metric("Boeing Commercial Server", "skew.boeing.commercial", delta="ACTIVE" if seal_health["status"] == "NOMINAL" else "HALTED", delta_color="normal" if seal_health["status"] == "NOMINAL" else "inverse")

    # 3. Handle Interactive Emergency Visual UI Changes
    if seal_health["status"] == "CRITICAL":
        st.error(f"CRITICAL SEAL LEAK DETECTED! Executing Strategy: **{security_action['action']}**")
        st.info(f"Action Protocol: {security_action['instructions']}")
    else:
        st.success(f"Enclosure Sealed. Status: {seal_health['message']}")

    # 4. Compile Consolidated Data Payload Array
    cad_payload = {
        "wingspan": wing_span,
        "seal_pressure": simulated_pressure,
        "security_state": security_action["action"],
        "timestamp": time.time()
    }
    
    # Convert flags directly into JavaScript sandbox variables
    blank_viewport_flag = "true" if security_action["action"] in ["BLANK_VIEWPORT", "HARD_LOCK", "REVERSE_INJECTION"] else "false"
    disable_inputs_flag = "true" if security_action["action"] in ["HARD_LOCK", "REVERSE_INJECTION"] else "false"

    # 5. Dual-Domain Embedded CAD Viewports
    st.subheader("Live Cross-Corporate AutoCAD Synchronizer")
    
    cad_html_component = f"""
    <div style="display: flex; gap: 20px; font-family: monospace;">
        <!-- Lockheed Martin Viewport -->
        <div style="flex: 1; border: 2px solid #333; background: #111; padding: 10px; border-radius: 6px;">
            <div style="color: #00ff00; margin-bottom: 8px;">CAD FEED: interface.01_node_ca.lockheedmartin.com</div>
            <div id="lockheed-container" style="height: 450px; background: #1a1a1a; display: flex; align-items: center; justify-content: center; position: relative;">
                <iframe id="lockheed-frame" src="https://autocad.com" style="width:100%; height:100%; border:none; display: {'none' if blank_viewport_flag == 'true' else 'block'};"></iframe>
                <div id="lockheed-lockout" style="position: absolute; color: #ff0000; font-weight: bold; display: {'block' if blank_viewport_flag == 'true' else 'none'};">VIEWPORT BLANKED BY SECURITY POLICY</div>
            </div>
        </div>
        
        <!-- Boeing Viewport -->
        <div style="flex: 1; border: 2px solid #333; background: #111; padding: 10px; border-radius: 6px;">
            <div style="color: #00ff00; margin-bottom: 8px;">CAD FEED: skew.boeing.commercial.boeing.com</div>
            <div id="boeing_container" style="height: 450px; background: #1a1a1a; display: flex; align-items: center; justify-content: center; position: relative;">
                <iframe id="boeing-frame" src="https://autocad.com" style="width:100%; height:100%; border:none; display: {'none' if blank_viewport_flag == 'true' else 'block'};"></iframe>
                <div id="boeing-lockout" style="position: absolute; color: #ff0000; font-weight: bold; display: {'block' if blank_viewport_flag == 'true' else 'none'};">VIEWPORT BLANKED BY SECURITY POLICY</div>
            </div>
        </div>
    </div>

    <script>
        const payload = {json.dumps(cad_payload)};
        const lockValue = {disable_inputs_flag};
        
        // Transmit updates directly to corporate endpoints via browser event pipeline
        function broadcastToDomains() {{
            const lmFrame = document.getElementById('lockheed-frame');
            const boeingFrame = document.getElementById('boeing-frame');
            
            if(lmFrame && lmFrame.contentWindow && !lockValue) {{
                lmFrame.contentWindow.postMessage({{ type: "MODEL_UPDATE", data: payload }}, "https://interface.01_node_ca.lockheedmartin.com");
            }}
            if(boeingFrame && boeingFrame.contentWindow && !lockValue) {{
                boeingFrame.contentWindow.postMessage({{ type: "MODEL_UPDATE", data: payload }}, "https://boeing.com");
            }}
        }}
        
        window.onload = broadcastToDomains;
    </script>
    """
    components.html(cad_html_component, height=520, scrolling=False)

if __name__ == "__main__":
    render_aerospace_cockpit()
