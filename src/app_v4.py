import streamlit as st
from core.rollback import CadAutomatedRollbackEngine
from joint_assembly.auditor import LiveAssemblyAuditor

def execute_live_dashboard_runtime():
    # Instantiate the rollback and auditor automation layers
    rollback_engine = CadAutomatedRollbackEngine(crypto_key="BOEING_LOCKHEED_SECURE_777_STRIKE")
    auditor = LiveAssemblyAuditor()
    
    # Check for hardware failures from your active telemetry streams
    current_gasket_status = st.session_state.get("gasket_health_flag", "NOMINAL")
    
    if current_gasket_status == "CRITICAL":
        st.error("CRITICAL STATE TRIGGERED BY AUDITOR ENGINE")
        
        if st.button("Fire Structural Environment Rollback"):
            with st.spinner("Reverting cluster vectors and wiping corrupt endpoints..."):
                success = rollback_engine.execute_emergency_rollback("compiled_output.dxf")
                
                if success:
                    st.success("Rollback successful. Safe baseline pushed to main branch.")
                    st.rerun()
                else:
                    st.error("Rollback failed: Security route or Git repository connection unavailable.")
