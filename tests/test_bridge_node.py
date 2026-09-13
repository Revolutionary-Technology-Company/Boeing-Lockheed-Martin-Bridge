import pytest
import numpy as np
from src.core.hex_logic import HexadecimalVoltageMatrix
from src.core.gasket_telemetry import ACDelcoGasketMonitor
from src.core.hex_exporter import HexFormatExporter

def test_hexadecimal_voltage_matrix():
    matrix = HexadecimalVoltageMatrix()
    # Test perfect intervals corresponding to 0x0 and 0xF
    assert matrix.decode_signal(0.0) == "0"
    assert matrix.decode_signal(1.0) == "F"
    # Test dynamic stream mapping logic
    assert matrix.process_telemetry_stream([0.0, 1.0, 0.5]) == "0F8"

def test_gasket_telemetry():
    monitor = ACDelcoGasketMonitor(target_pressure=50.0)
    # Check stable pressure boundary
    assert monitor.verify_seal_integrity(48.0)["status"] == "NOMINAL"
    # Check compression leak exception boundary
    assert monitor.verify_seal_integrity(20.0)["status"] == "CRITICAL"

def test_hex_exporter(tmpdir):
    exporter = HexFormatExporter(output_dir=str(tmpdir))
    hex_sample = "41424344" # Representing ASCII 'ABCD'
    
    bin_path = exporter.save_as_binary_fragment("test_payload", hex_sample)
    assert bin_path.endswith(".bin")
    
    hex_path = exporter.save_as_readable_table("test_table", hex_sample, columns=2)
    assert hex_path.endswith(".hex")
