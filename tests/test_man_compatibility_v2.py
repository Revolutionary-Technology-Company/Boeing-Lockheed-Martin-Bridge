import pytest
from src.man_powertrain.j1939_parser import ManSurfacePanelsParser

def test_man_surface_panel_displacement_parsing():
    parser = ManSurfacePanelsParser()
    
    # Emulate an 8-byte J1939 CAN frame containing planar measurements
    # Payload short integers: [12, -5, 8, 1500] -> scaled by 0.001 multiplier
    mock_payload = b'\x0C\x00\xFB\xFF\x08\x00\xDC\x05'
    extended_can_id = 0x18FEE012
    
    parsed_output = parser.decode_panel_geometry_frame(extended_can_id, mock_payload)
    
    assert parsed_output["origin"] == "MAN_SURFACES"
    metrics = parsed_output["surface_metrics"]
    assert metrics["planar_displacement_x_mm"] == 0.012
    assert metrics["planar_displacement_y_mm"] == -0.005
    assert metrics["panel_edge_gap_mm"] == 0.008
    assert metrics["skin_shear_strain_microstrain"] == 1500.0
    assert parsed_output["structural_conformity"] is True
