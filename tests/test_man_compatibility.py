import pytest
from src.man_powertrain.j1939_parser import ManJ1939CanParser

def test_j1939_can_bus_parsing():
    parser = ManJ1939CanParser()
    
    # Emulate an 8-byte J1939 CAN bus frame payload chunk
    # Extended CAN ID example: 0x18FEE000 (Priority 6, PGN 65248 [Engine Fluid Level/Pressure], Source Address 0)
    mock_payload = b'\x4A\x12\xC6\x2F\x0F\xAA\x02\x40'
    extended_can_id = 0x18FEE000
    
    parsed_output = parser.decode_j1939_frame(extended_can_id, mock_payload)
    
    assert parsed_output["origin"] == "MAN_INDUSTRIAL"
    assert parsed_output["priority"] == 6
    assert parsed_output["parameter_group_number"] == 65248
    assert parsed_output["telemetry_matrix_hex"] == "4a12c62f0faa0240"
    assert parsed_output["structural_conformity"] is True
