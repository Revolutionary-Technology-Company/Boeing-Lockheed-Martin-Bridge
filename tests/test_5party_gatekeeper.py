import pytest
from src.joint_assembly.nda_gatekeeper import NDAGatekeeper

def test_five_party_gatekeeper_nominal_success(tmpdir):
    gatekeeper = NDAGatekeeper(shared_directory=str(tmpdir))
    
    assert gatekeeper.initialize_joint_aerospace_workspace(
        project_name="NASA_Artemis_Structure",
        boeing_sig="BOEING_RSA_KEY_8300_VALID",
        lockheed_sig="LOCKHEED_RSA_KEY_955_VALID",
        ab_sig="AB_CIP_TAG_CONN_VALID",
        man_sig="MAN_J1939_SURFACE_VALID",
        nasa_sig="NASA_CFS_CCSDS_APID_VALID"
    ) is True

def test_five_party_gatekeeper_revoked_token(tmpdir):
    gatekeeper = NDAGatekeeper(shared_directory=str(tmpdir))
    
    with pytest.raises(PermissionError) as exc_info:
        gatekeeper.initialize_joint_aerospace_workspace(
            project_name="NASA_Artemis_Structure",
            boeing_sig="BOEING_RSA_KEY_8300_VALID",
            lockheed_sig="LOCKHEED_RSA_KEY_955_VALID",
            ab_sig="AB_CIP_TAG_CONN_VALID",
            man_sig="MAN_J1939_SURFACE_REVOKED", # Invalid token
            nasa_sig="NASA_CFS_CCSDS_APID_VALID"
        )
    assert "Invalid signature token" in str(exc_info.value)
