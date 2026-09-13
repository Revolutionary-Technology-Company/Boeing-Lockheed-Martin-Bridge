import json
import re
import os
import hashlib
from datetime import datetime

def build_project_and_log_ledger(json_path, scad_path, ledger_path="project_ledger.json"):
    # 1. Parse JSON configs
    with open(json_path, 'r') as f:
        metrics = json.load(f)
        
    # 2. Format OpenSCAD Array Syntax
    array_elements = []
    for st in metrics["standoffs"]:
        array_elements.append(f"    [{st['x']}, {st['y']}, {st['inner_dia']}, {st['outer_dia']}, {st['height']}]")
    matrix_string = "standoff_matrix = [\n" + ",\n".join(array_elements) + "\n];"

    # 3. Read and replace metrics inside the .scad template code
    with open(scad_path, 'r') as f:
        scad_content = f.read()

    # Replace basic structural bounds
    for key in ["casing_length", "casing_width", "casing_height", "wall_thickness", "flange_width", "flange_thickness"]:
        scad_content = re.sub(rf"^({key}\s*=\s*)[^;]+;", f"\\1{metrics[key]};", scad_content, flags=re.MULTILINE)
        
    # Replace dynamic standoff matrix target blocks explicitly
    scad_content = re.sub(r"standoff_matrix\s*=\s*\[[\s\S]*?\]\s*;", matrix_string, scad_content)

    with open(scad_path, 'w') as f:
        f.write(scad_content)
    print(f"[✓] Dynamic fitting variables parsed into '{scad_path}'.")

    # 4. Process Ledger Auditing Record
    ledger_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "configuration_hash": hashlib.sha256(json.dumps(metrics, sort_keys=True).encode()).hexdigest(),
        "dimensions": {
            "box": f"{metrics['casing_length']}x{metrics['casing_width']}x{metrics['casing_height']}",
            "standoff_count": len(metrics["standoffs"])
        }
    }
    
    ledger_data = []
    if os.path.exists(ledger_path):
        try:
            with open(ledger_path, 'r') as f:
                ledger_data = json.load(f)
        except json.JSONDecodeError:
            pass
            
    ledger_data.append(ledger_entry)
    with open(ledger_path, 'w') as f:
        json.dump(ledger_data, f, indent=2)
    print(f"[✓] Structural update recorded to append-only shared ledger index '{ledger_path}'.")

if __name__ == "__main__":
    build_project_and_log_ledger("bridge_dimensions.json", "enclosure_mold.scad")
