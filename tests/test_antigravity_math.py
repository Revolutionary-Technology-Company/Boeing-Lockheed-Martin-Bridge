import pytest
from src.core.antigravity_core import ACDelcoAntigravityEngine

def test_electrostatic_lift_physics():
    # Instantiate the engine with a standard 1-metric-ton vessel profile
    engine = ACDelcoAntigravityEngine(vessel_mass_kg=1000.0)
    
    # Assert that the lift calculation matches exactly 98 Coulombs
    assert engine.calculate_required_hover_charge() == 98.0
    
    # Assert that no charge potential results in the baseline 0 Hex state
    assert engine.map_plate_potential_to_hex(0.0) == "0"
    
    # Assert that a complete charge saturation maps to maximum State F
    assert engine.map_plate_potential_to_hex(120.0) == "F"
