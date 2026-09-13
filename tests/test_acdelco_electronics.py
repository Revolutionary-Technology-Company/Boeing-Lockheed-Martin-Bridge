import pytest
from src.acdelco_wiring_harness import ACDelcoWiringHarness
from src.boeing_telemetry_bridge import ACDelcoAviationBridge

def test_harness_voltage_scaling():
    harness = ACDelcoWiringHarness(baseline_resistance_ohms=0.1)
    # Perfect condition: No current flow equals no voltage drop (1.0V -> State F)
    v_nominal = harness.calculate_voltage_drop(current_amps=0.0)
    assert harness.convert_voltage_to_hex(v_nominal) == "F"

def test_bridge_critical_exception():
    bridge = ACDelcoAviationBridge()
    # High current load (3.0A) causes total circuit voltage crash -> State 0
    result = bridge.sync_hardware_to_climatology(raw_current_stream=[3.0, 0.0])
    assert result["hardware_integrity"] == "CRITICAL_VOLTAGE_DROP"
    assert result["telemetry_node_color"] == "EMERGENCY_RED"
