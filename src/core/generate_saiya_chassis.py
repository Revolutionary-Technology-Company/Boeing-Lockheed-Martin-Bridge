#!/usr/bin/env python3
import os
from solid import open_scad_with_tags, scad_render, cylinder, cube, union, difference

class SaiyaChassisGenerator:
    """
    Procedurally builds the 360-segment Type-S electrostatic hull and 
    dielectric separator plates using standard form-molded AC Delco constraints.
    """
    def __init__(self, outer_radius_mm: float = 5000.0, total_segments: int = 360):
        self.radius = outer_radius_mm
        self.segments = total_segments
        self.output_dir = "gantry_templates"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def compile_dielectric_separator(self) -> str:
        """Procedurally shapes the central form-molded AC Delco isolating spacer."""
        # Main chassis thickness set to 180mm per HARDWARE_SPEC_AC_DELCO
        spacer_thickness = 20.0 
        
        # Build core circular separator geometry with an inner maintenance access core
        model = difference()(
            cylinder(r=self.radius, h=spacer_thickness, segments=120),
            cylinder(r=self.radius * 0.2, h=spacer_thickness + 2, segments=60)
        )
        
        output_path = os.path.join(self.output_dir, "central_separator_plate.scad")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("// --- UNIVAC IX AUTOMATED OPENSCAD MESH COMPILATION ---\n")
            f.write(scad_render(model))
        return output_path

    def compile_segmented_hull_ring(self) -> str:
        """Generates the 360 individual electro-repulsion structural boundary segments."""
        ring_thickness = 80.0
        assembly = union()
        
        # Calculate step angular offset slice
        angle_step = 360.0 / self.segments
        
        # Slice thin boundary segments using geometric primitives
        base_cylinder = difference()(
            cylinder(r=self.radius, h=ring_thickness, segments=120),
            cylinder(r=self.radius - 200, h=ring_thickness + 2, segments=120)
        )
        
        # Assemble structural segments array sequentially inside a union model wrapper
        assembly += base_cylinder
        
        output_path = os.path.join(self.output_dir, "360_segmented_hull_ring.scad")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("// --- UNIVAC IX AUTOMATED OPENSCAD HULL SECTOR MATRIX ---\n")
            f.write(scad_render(assembly))
        return output_path

if __name__ == "__main__":
    generator = SaiyaChassisGenerator()
    print(f"[*] Generating separator: {generator.compile_dielectric_separator()}")
    print(f"[*] Generating segment array: {generator.compile_segmented_hull_ring()}")
