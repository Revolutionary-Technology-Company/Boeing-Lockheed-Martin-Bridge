import pytest
import os
from src.core.generate_saiya_chassis import SaiyaChassisGenerator

def test_procedural_scad_io(tmpdir):
    # Route generation to temporary virtual disk location
    generator = SaiyaChassisGenerator(outer_radius_mm=1000.0, total_segments=12)
    generator.output_dir = str(tmpdir)
    
    separator_file = generator.compile_dielectric_separator()
    hull_file = generator.compile_segmented_hull_ring()
    
    assert os.path.exists(separator_file)
    assert os.path.exists(hull_file)
    
    with open(separator_file, "r") as f:
        content = f.read()
    assert "cylinder" in content
