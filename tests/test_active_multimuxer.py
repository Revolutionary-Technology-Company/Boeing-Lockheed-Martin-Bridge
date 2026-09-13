import pytest
import numpy as np
from src.core.active_multimuxer import ActiveBridgeMultimuxer

def test_multimuxer_channel_compression():
    mux = ActiveBridgeMultimuxer()
    
    # Emulate 6 simultaneous enterprise channel lines containing data
    mock_6_channels = np.full((50, 6), 150.0, dtype=np.float32)
    
    # Execute multiplexing step
    output = mux.multiplex_corporate_inputs(mock_6_channels)
    
    assert output["origin"] == "ACTIVE_MULTIMUXER_CORE"
    assert output["active_code_buffers_replaced"] == 6
    assert len(output["multiplexed_signal_vector"]) == 50
    assert output["structural_conformity"] is True

def test_demultiplexer_output_distribution():
    mux = ActiveBridgeMultimuxer()
    single_signal_stream = np.array([100.0, 100.0, 100.0], dtype=np.float32)
    
    # Demultiplex to target device terminal index 2
    device_feed = mux.demultiplex_to_device(single_signal_stream, target_device_idx=2)
    
    assert len(device_feed) == 3
    assert device_feed[0] == 110.0  # 100.0 * (1.0 + 0.05 * 2)
