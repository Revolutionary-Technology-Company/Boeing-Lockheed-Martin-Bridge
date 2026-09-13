import pytest
from src.ab_automation.cip_parser import AllenBradleyCipParser

def test_cip_dint_tag_parsing():
    parser = AllenBradleyCipParser()
    
    # Emulate a successful CIP Read Tag Response for a DINT value of 15000
    # Service Response: 0xCC | Status: 0x00 | Type: 0xC4 0x00 (DINT) | Data: Value 15000 (\x98\x3A\x00\x00)
    mock_packet = b'\xCC\x00\xC4\x00\x98\x3A\x00\x00'
    
    parsed_output = parser.parse_cip_read_tag_response(mock_packet)
    
    assert parsed_output["origin"] == "ALLEN_BRADLEY"
    assert parsed_output["status"] == "NOMINAL"
    assert parsed_output["ab_data_type"] == "DINT"
    assert parsed_output["decoded_value"] == 15000
    assert parsed_output["structural_conformity"] is True

def test_cip_error_handling():
    parser = AllenBradleyCipParser()
    
    # Emulate an error packet where Byte 1 indicates a routing failure (e.g., 0x04 - Tag Not Found)
    mock_error_packet = b'\xCC\x04\x00\x00'
    
    parsed_output = parser.parse_cip_read_tag_response(mock_error_packet)
    
    assert parsed_output["status"] == "CIP_ERROR"
    assert parsed_output["error_code"] == "4"
    assert parsed_output["structural_conformity"] is False
