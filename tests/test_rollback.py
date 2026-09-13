import pytest
import os
from src.core.rollback import CadAutomatedRollbackEngine

def test_checkpoint_and_rollback_flow(tmpdir):
    engine = CadAutomatedRollbackEngine(workspace_directory=str(tmpdir), crypto_key="ROLLBACK_TEST_KEY")
    filename = "compiled_output.dxf"
    active_filepath = os.path.join(str(tmpdir), filename)
    
    # Create an initial nominal drawing file
    with open(active_filepath, "w") as f:
        f.write("NOMINAL_PARAM=15000")
        
    # Checkpoint the safe system baseline state
    checkpoint_path = engine.checkpoint_current_stable_state(filename)
    assert os.path.exists(checkpoint_path)
    
    # Simulate a system engineer introducing corrupt or unaligned design values
    with open(active_filepath, "w") as f:
        f.write("CORRUPTED_PARAM=99999")
        
    # Trigger the automated rescue loop
    engine.execute_emergency_rollback(filename)
    
    # Verify that the active configuration file has reverted back to the safe state
    with open(active_filepath, "r") as f:
        content = f.read()
    assert "NOMINAL_PARAM=15000" in content
    assert "CORRUPTED_PARAM" not in content
