import pytest
import numpy as np
from src.core.fire_cuda_engine import FireWatchCudaEngine

def test_cuda_engine_nominal_matrix():
    engine = FireWatchCudaEngine(target_threshold=150.0)
    
    # Create low baseline telemetry matrix array
    nominal_matrix = np.full((16, 16), 25.0, dtype=np.float32)
    output = engine.evaluate_array_on_gpu(nominal_matrix)
    
    assert output["origin"] == "FIREWATCH_CUDA_ENGINE"
    assert output["incident_verification"] == "NOMINAL_STABLE"
    assert output["structural_conformity"] is True

def test_cuda_engine_surge_matrix():
    engine = FireWatchCudaEngine(target_threshold=150.0)
    
    # Create an array that breaches safe thermal limits
    surge_matrix = np.full((16, 16), 195.0, dtype=np.float32)
    output = engine.evaluate_array_on_gpu(surge_matrix)
    
    assert output["incident_verification"] == "CRITICAL_THERMAL_SURGE"
    assert output["ui_node_color"] == "EMERGENCY_RED"
    assert output["structural_conformity"] is False
