import pytest
from src.core.bridge_gravity_induction import BridgeGravityInductionEngine

def test_bridge_gravity_differential_math():
    engine = BridgeGravityInductionEngine(target_gravity_g=1.0)
    
    # Verify absolute baseline nominal conditions (45C and -45C = 1.0G)
    nominal_output = engine.calculate_bridge_field_differential(45.0, -45.0)
    assert nominal_output["bridge_field_status"] == "NOMINAL_STABLE"
    assert nominal_output["induced_g_force_magnitude"] == 1.0
    assert nominal_output["hex_voltage_state"] == "0.FV"  
    
    # Verify degraded output drop conditions
    low_output = engine.calculate_bridge_field_differential(20.0, -20.0)
    assert low_output["bridge_field_status"] == "DEGRADED_GRAVITY_FIELD"
    assert low_output["induced_g_force_magnitude"] < 0.5
    
    # Verify failure loop on polarity short circuits
    fault_output = engine.calculate_bridge_field_differential(-10.0, 10.0)
    assert fault_output["bridge_field_status"] == "CRITICAL_POLARITY_INVERSION"
    assert fault_output["structural_conformity"] is False
