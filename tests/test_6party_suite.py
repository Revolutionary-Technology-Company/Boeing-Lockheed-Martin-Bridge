import pytest
from src.joint_assembly.nda_gatekeeper import NDAGatekeeper
from src.ng_tactical.message_generator import Link16MessageGenerator
from src.ng_tactical.link16_parser import NorthropGrummanLink16Parser

def test_six_party_gatekeeper_enforcement(tmpdir):
    gatekeeper = NDAGatekeeper(shared_directory=str(tmpdir))
    
    # Assert successful validation with all six required keys
    assert gatekeeper.initialize_joint_aerospace_workspace(
        project_name="Project_Artemis_Stratum",
        boeing_sig="BOEING_8300_VALID",
        lockheed_sig="LOCKHEED_955_VALID",
        ab_sig="AB_CIP_VALID",
        man_sig="MAN_J1939_VALID",
        nasa_sig="NASA_CCSDS_VALID",
        ng_sig="NG_LINK16_VALID"
    ) is True

def test_link16_generator_to_parser_loop():
    generator = Link16MessageGenerator(baseline_track_id=512)
    parser = NorthropGrummanLink16Parser()
    
    # Run loop check: pack data, slice byte buffers, decode, and match properties
    raw_packet = generator.generate_live_j2_packet(base_coordinate=700.0)
    parsed_output = parser.parse_j_series_track_packet(raw_packet)
    
    assert parsed_output["origin"] == "NORTHROP_GRUMMAN"
    assert parsed_output["link16_label"] == "J2.2"
    assert parsed_output["source_track_id"] == "200" # 512 in hex is 0x200
    assert 0.0 <= parsed_output["scaled_displacement_factor"] <= 1.0
    assert parsed_output["structural_conformity"] is True
