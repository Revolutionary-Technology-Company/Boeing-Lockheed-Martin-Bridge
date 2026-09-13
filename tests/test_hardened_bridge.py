import pytest
import os
from src.core.autocad_bridge import AutoCADProductBridge

def test_production_encryption_loop(tmpdir):
    bridge = AutoCADProductBridge(workspace_directory=str(tmpdir), crypto_key="CONFIDENTIAL_TEST_PHRASE")
    
    # Write sample design metrics
    filename = "test_cad_data.dxf"
    with open(os.path.join(str(tmpdir), filename), "w") as f:
        f.write("LAYER_DATA: WING_BOX_MOLD=TRUE")
        
    # Execute structural encryption step
    encrypted_path = bridge.encrypt_production_file(filename)
    
    assert os.path.exists(encrypted_path)
    assert encrypted_path.endswith(".enc")
    
    # Confirm text is unreadable directly from disk storage
    with open(encrypted_path, "r", encoding="utf-8", errors="ignore") as f:
        encrypted_raw_text = f.read()
    assert "WING_BOX_MOLD" not in encrypted_raw_text
