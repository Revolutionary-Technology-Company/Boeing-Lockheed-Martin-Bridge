import streamlit as st
import os
from core.generate_thruster_mesh import FinalBridgeThrusterGenerator
from core.render_stl_mesh import OpenScadMeshCompiler

def render_mesh_compilation_dashboard():
    st.subheader("🛠️ Production Manufacturing & Gantry Mesh Compiler")
    st.caption("Headless CAD Engine Integration for 3D Printable STL Output")

    # Instantiate compilers inside the loop
    generator = FinalBridgeThrusterGenerator(fundamental_frequency_hz=13.72)
    compiler = OpenScadMeshCompiler()

    col_build, col_status = st.columns([1, 2])
    
    with col_build:
        if st.button("🏗️ Compile & Render 3D Printable STL Mesh"):
            with st.spinner("Executing SolidPython geometry synthesis..."):
                # Step 1: Generate updated .scad source model text file
                scad_path = generator.compile_production_mesh()
                scad_file = os.path.basename(scad_path)
                
                # Step 2: Stream text vectors directly through the local OpenSCAD compiler binary
                stl_output_path = compiler.export_scad_to_stl(scad_file)
                
                if stl_output_path:
                    st.success("✅ 3D Mesh Compiled Successfully!")
                    st.session_state["last_compiled_mesh"] = stl_output_path
                else:
                    st.error("❌ Mesh Compilation Interrupted. Check CLI logs.")
                    
    with col_status:
        if "last_compiled_mesh" in st.session_state:
            st.info(f"💾 Active Production Artifact:\n`{st.session_state['last_compiled_mesh']}`")
            # Present file size parameters to verify unmanaged data shape density
            size_bytes = os.path.getsize(st.session_state["last_compiled_mesh"])
            st.text(f"File footprint density: {size_bytes / (1024*1024):.2f} MB")
