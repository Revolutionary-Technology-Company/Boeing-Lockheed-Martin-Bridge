import pytest
from src.joint_assembly.nda_gatekeeper import NDAGatekeeper

def test_tri_corporate_gatekeeper_success(tmpdir):
    gatekeeper = NDAGatekeeper(shared_directory=str(tmpdir))
    
    # Verify nominal three-party authorization loop
    assert gatekeeper.initialize_tri_corporate_project(
        project_name="Project_Apex_Airframe_Powertrain",
        boeing_sig="BOEING_RSA_KEY_8300_VALID",
        lockheed_sig="LOCKHEED_RSA_KEY_955_VALID",
        gm_sig="GM_GMLAN_MATRIX_J1939_VALID"
    ) is True

def test_tri_corporate_gatekeeper_missing_signature(tmpdir):
    gatekeeper = NDAGatekeeper(shared_directory=str(tmpdir))
    
    # Assert failure when one company (GM) fails to sign
    with pytest.raises(PermissionError) as exc_info:
        gatekeeper.initialize_tri_corporate_project(
            project_name="Project_Apex_Airframe_Powertrain",
            boeing_sig="BOEING_RSA_KEY_8300_VALID",
            lockheed_sig="LOCKHEED_RSA_KEY_955_VALID",
            gm_sig=""  # Empty signature
        )
    assert "Incomplete cryptographic handshake" in str(exc_info.value)
