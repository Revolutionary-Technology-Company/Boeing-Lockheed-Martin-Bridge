import os
import json
import re

class AutoCADProductBridge:
    """
    Handles programmatic data synchronization with AutoCAD products, vector files, 
    assembly directories, and shared design blocks.
    """
    def __init__(self, workspace_directory: str = "./joint_projects"):
        self.workspace_dir = workspace_directory
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def extract_dxf_layers(self, file_name: str) -> dict:
        """
        Parses raw text layers of an AutoCAD DXF file to identify 
        mating slot clearances and wing assembly entities.
        """
        file_path = os.path.join(self.workspace_dir, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CAD File Asset missing at: {file_path}")

        layers = {}
        current_layer = "UNKNOWN"
        
        with open(file_path, "r", encoding="utf-8", errors="ignore") as dxf:
            lines = [line.strip() for line in dxf.readlines()]
            
        for i in range(len(lines)):
            if lines[i] == "8" and (i + 1) < len(lines):  # Group code 8 indicates Layer Name
                current_layer = lines[i + 1]
                if current_layer not in layers:
                    layers[current_layer] = 0
            elif lines[i] == "AcDbEntity" and current_layer != "UNKNOWN":
                layers[current_layer] += 1
                
        return {"file": file_name, "detected_layers": layers}

    def inject_live_parameters_to_dxf(self, input_file: str, output_file: str, wingspan: float) -> str:
        """
        Locates specific dimension variables inside a target template DXF vector matrix 
        and updates values in real time based on application input slider events.
        """
        in_path = os.path.join(self.workspace_dir, input_file)
        out_path = os.path.join(self.workspace_dir, output_file)
        
        if not os.path.exists(in_path):
            raise FileNotFoundError(f"Source baseline template not found at {in_path}")

        with open(in_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Target explicit user-defined hardware metadata keys inside CAD comment spaces
        # Format matching: %%[WINGSPAN_VAL]%%
        updated_content = re.sub(r"%%\[WINGSPAN_VAL\]%%", f"{wingspan:.4f}", content)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        return out_path

    def catalog_project_directory(self) -> list:
        """Audits the active joint workspace and maps out current file objects."""
        cad_objects = []
        for root, _, files in os.walk(self.workspace_dir):
            for file in files:
                if file.lower().endswith(('.dxf', '.dwg', '.json')):
                    full_path = os.path.join(root, file)
                    cad_objects.append({
                        "name": file,
                        "size_bytes": os.path.getsize(full_path),
                        "extension": file.split(".")[-1].upper()
                    })
        return cad_objects
