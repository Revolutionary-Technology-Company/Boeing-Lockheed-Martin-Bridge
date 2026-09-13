import pytest
from src.gm_powertrain.gmlan_parser import GMLanCanBusParser

def test_gmlan_can_bus_parsing():
    parser = GMLanCanBusParser()
    
    # Emulate an 8-byte automotive CAN bus frame payload chunk
    mock_payload = b'\x00\x12\xD6\x87\x0F\xAA\x02\x40'
    can_arbitration_id = 0x18DAF110
    
    parsed_output = parser.parse_gmlan_frame(can_arbitration_id, mock_payload)
    
    assert parsed_output["origin"] == "GENERAL_MOTORS"
    assert parsed_output["can_arbitration_id"] == "18DAF110"
    assert parsed_output["telemetry_matrix_hex"] == "0012D6870FAA0240"
    assert parsed_output["structural_conformity"] is True
