import os
import subprocess

class OpenScadMeshCompiler:
    """
    Programmatically interfaces Python design automation loops with local 
    OpenSCAD CLI binaries. Renders solid vector drawings into hard, 
    production-ready 3D printable STL polygon geometry meshes.
    """
    def __init__(self, templates_dir: str = "gantry_templates", export_dir: str = "docs/mesh_exports"):
        self.templates_dir = templates_dir
        self.export_dir = export_dir
        
        # Enforce strict directory allocation for output build layers
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def export_scad_to_stl(self, scad_filename: str) -> str:
        """
        Executes a headless shell process command to render a target .scad file 
        directly into a hard 3D printable STL polygon geometry mesh layer.
        """
        source_scad = os.path.join(self.templates_dir, scad_filename)
        output_stl = os.path.join(self.export_dir, scad_filename.replace(".scad", ".stl"))
        
        if not os.path.exists(source_scad):
            raise FileNotFoundError(f"Source CAD text template missing at: {source_scad}")

        print(f"[*] Initializing headless OpenSCAD processor for {scad_filename}...")
        
        # Build strict headless CLI command configuration line to match production runtimes
        command = [
            "openscad",
            "-o", output_stl,
            source_scad
        ]
        
        try:
            # Dispatch command pipeline into isolated subprocess execution boundaries
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"[+] Mesh compilation successful: {output_stl}")
            return output_stl
        except subprocess.CalledProcessError as e:
            print(f"[-] OpenSCAD Binary Execution Failure: {e.stderr if e.stderr else str(e)}")
            return ""
