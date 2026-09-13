import pytest
import os
from src.core.autocad_bridge import AutoCADProductBridge

def test_cad_directory_mapping(tmpdir):
    # Setup temporary mocked CAD file directory
    bridge = AutoCADProductBridge(workspace_directory=str(tmpdir))
    
    # Write a dummy mock DXF structure to disk
    mock_file = os.path.join(str(tmpdir), "test_wing_template.dxf")
    with open(mock_file, "w") as f:
        f.write("0\nSECTION\n2\nHEADER\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\nLINE\n8\nBOEING_FRAME_LAYER\n%%[WINGSPAN_VAL]%%\n0\nENDSEC\n0\nEOF")
        
    catalog = bridge.catalog_project_directory()
    assert len(catalog) == 1
    assert catalog[0]["name"] == "test_wing_template.dxf"

    # Test live parameter search-and-replace injection loop
    output_path = bridge.inject_live_parameters_to_dxf("test_wing_template.dxf", "output_compiled.dxf", 15450.50)
    with open(output_path, "r") as f:
        result_content = f.read()
    assert "15450.5000" in result_content
