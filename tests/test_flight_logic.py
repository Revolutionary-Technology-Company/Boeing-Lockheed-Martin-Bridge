import pytest
import os
import numpy as np
from src.core.bak_flight_controller import SaiyaFlightController
from src.core.render_stl_mesh import OpenScadMeshCompiler

def test_flight_vector_bias_shifting():
    controller = SaiyaFlightController(target_hover_charge=98.0)
    
    # Calculate matrix with zero bias (flat hover state)
    flat_matrix = controller.compute_steering_matrix(target_heading_degrees=0, maneuver_intensity=0.0)
    assert np.allclose(flat_matrix, 98.0 / 360.0)

    # Calculate biased vector pointing straight at sector position 90
    biased_matrix = controller.compute_steering_matrix(target_heading_degrees=90, maneuver_intensity=0.2)
    # The plate at index 90 must maintain higher charge density than the opposing plate at index 270
    assert biased_matrix[90] > biased_matrix[270]

def test_headless_mesh_compiler_exceptions():
    compiler = OpenScadMeshCompiler()
    # Confirm module catches file paths errors securely
    with pytest.raises(FileNotFoundError):
        compiler.export_scad_to_stl("non_existent_chassis_mock.scad")
