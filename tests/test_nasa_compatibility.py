import pytest
from src.nasa_ops.ccsds_parser import NasaCcsdsSpaceParser

def test_ccsds_primary_header_parsing():
    parser = NasaCcsdsSpaceParser()
    
    # Mock a 6-byte telemetry packet header chunk:
    # Binary pattern representing: Version 0, Type 0, Sec Header 0, APID 452 (0x01C4) | Seq Count 2048 | Data Length parameter 63 (64 bytes total)
    mock_ccsds_header = b'\x01\xC4\x08\x00\x00\x3F'
    
    parsed_output = parser.parse_ccsds_header(mock_ccsds_header)
    
    assert parsed_output["origin"] == "NASA_OPERATIONS"
    assert parsed_output["application_process_id_apid"] == 452
    assert parsed_output["packet_sequence_count"] == 2048
    assert parsed_output["payload_data_length_bytes"] == 64
    assert parsed_output["structural_conformity"] is True
