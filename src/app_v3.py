import streamlit as st
import os
from core.autocad_bridge import AutoCADProductBridge

def render_hardened_deployment_dashboard():
    st.subheader("Hardened Production Synchronization Controls")
    
    # Instantiate the upgraded file engine
    crypto_secret = os.getenv("CRYPTO_KEY_SIGNATURE", "BOEING_LOCKHEED_SECURE_777_STRIKE")
    cad_bridge = AutoCADProductBridge(crypto_key=crypto_secret)
    
    wing_span = st.slider("Dynamic Airframe Wing Dimension (mm)", 12000.0, 18000.0, 15000.0, step=0.5)
    
    if st.button("Push Verified Changes Live to Main Branch"):
        with st.spinner("Processing architectural data conversion layer..."):
            
            # 1. Update the AutoCAD physical drawing parameters
            raw_dxf = cad_bridge.inject_live_parameters_to_dxf("template.dxf", "compiled_output.dxf", wing_span)
            st.success(f"Step 1: CAD File Matrix Updated Local Template.")
            
            # 2. Encrypt files before writing to the shared workspace volume
            encrypted_file = cad_bridge.encrypt_production_file("compiled_output.dxf")
            st.success(f"Step 2: Created Secure AES-256 Storage Artifact: `{os.path.basename(encrypted_file)}`")
            
            # 3. Synchronize with the live repository main branch
            sync_success = cad_bridge.commit_and_push_to_main(
                target_filename="compiled_output.dxf.enc", 
                commit_message=f"Synchronized wing component scaling parameters to {wing_span}mm."
            )
            
            if sync_success:
                st.balloons()
                st.success("Step 3: Complete Cluster Synchronized! Main branch updated successfully.")
            else:
                st.error("Step 3 Failure: Network Route Boundary Denied Git Repository Broadcast Access.")
