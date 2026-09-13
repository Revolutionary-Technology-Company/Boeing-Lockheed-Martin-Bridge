import pytest
import numpy as np
from src.core.fire_cuda_engine import FireWatchHardwareEngine

def test_multicore_cpu_fallback_pathway():
    engine = FireWatchHardwareEngine(target_threshold=150.0)
    nominal_matrix = np.full((32, 32), 25.0, dtype=np.float32)
    
    # Force Multi-Core execution path directly to evaluate OpenMP thread stability
    output = engine.process_matrix_frame(nominal_matrix, force_cpu=True)
    
    assert output["active_hardware_engine"] == "MULTICORE_PARALLEL_CPU"
    assert output["incident_verification"] == "NOMINAL_STABLE"
    assert output["structural_conformity"] is True

def test_hardware_surge_response():
    engine = FireWatchHardwareEngine(target_threshold=150.0)
    surge_matrix = np.full((32, 32), 210.0, dtype=np.float32)
    
    output = engine.process_matrix_frame(surge_matrix, force_cpu=True)
    
    assert output["incident_verification"] == "CRITICAL_THERMAL_SURGE"
    assert output["structural_conformity"] is False
