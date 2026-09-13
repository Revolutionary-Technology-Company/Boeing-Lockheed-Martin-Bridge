import pytest
from src.core.avionics_bridge import HyperTomcatAvionicsBridge

def test_legacy_36bit_word_parsing():
    bridge = HyperTomcatAvionicsBridge()
    
    # Construct a legacy 36-bit word representing a middle balance calibration state:
    # Boeing Airframe Field = 0x800 (2048) | Lockheed Avionics Field = 0x800 (2048) | Tactical Field = 0x000 (0)
    # Binary word layout evaluates to integer value: 8388608
    mock_word = (0x000 << 24) | (0x800 << 12) | 0x800
    
    parsed_output = bridge.parse_36bit_word(mock_word)
    
    assert parsed_output["origin"] == "HYPER_TOMCAT_AVIONICS"
    assert parsed_output["boeing_airframe_status_field"] == "800"
    assert parsed_output["lockheed_avionics_vector_field"] == "800"
    assert parsed_output["hex_voltage_state"] == "0.8V"  # 2048 / 4095 scales to exactly half of 1.0V (0.5V step closest matching index)
    assert parsed_output["structural_conformity"] is True
