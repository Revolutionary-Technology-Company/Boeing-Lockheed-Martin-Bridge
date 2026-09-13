import pytest
import os
from src.core.generate_thruster_mesh import FinalBridgeThrusterGenerator
from src.core.render_stl_mesh import OpenScadMeshCompiler

def test_headless_mesh_compiler_pipeline(tmpdir):
    # Setup isolated test directory directories
    test_templates_dir = os.path.join(str(tmpdir), "gantry_templates")
    test_export_dir = os.path.join(str(tmpdir), "docs/mesh_exports")
    os.makedirs(test_templates_dir)
    
    # 1. Instantiate the generator and target temporary test paths
    generator = FinalBridgeThrusterGenerator(fundamental_frequency_hz=13.72)
    generator.output_dir = test_templates_dir
    scad_path = generator.compile_production_mesh()
    scad_filename = os.path.basename(scad_path)
    
    # 2. Instantiate compiler pointing to the virtual disk layout
    compiler = OpenScadMeshCompiler(templates_dir=test_templates_dir, export_dir=test_export_dir)
    
    # Assert exception path works if file goes missing
    with pytest.raises(FileNotFoundError):
        compiler.export_scad_to_stl("missing_mock_file.scad")
        
    # 3. Execute compilation process (Skipped if open-scad binary missing from test container paths)
    if os.system("command -v openscad > /dev/null 2>&1") == 0:
        stl_path = compiler.export_scad_to_stl(scad_filename)
        assert os.path.exists(stl_path)
        assert stl_path.endswith(".stl")
