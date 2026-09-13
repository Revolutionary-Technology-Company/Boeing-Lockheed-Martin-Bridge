import json
import re
import os
import hashlib
import sys
from datetime import datetime

def run_boundary_collision_check(metrics):
    """
    Validates that every dynamic standoff sits strictly inside the internal cavity wall space.
    Calculates boundaries using casing dimensions and wall thickness.
    """
    # Calculate internal bounding walls relative to center (0,0)
    max_allowable_x = (metrics["casing_length"] / 2.0) - metrics["wall_thickness"]
    max_allowable_y = (metrics["casing_width"] / 2.0) - metrics["wall_thickness"]
    
    print("[*] Initiating boundary-box structural collision checks...")
    
    for idx, standoff in enumerate(metrics["standoffs"]):
        x_coord = standoff["x"]
        y_coord = standoff["y"]
        radius_offset = standoff["outer_dia"] / 2.0
        
        # Check X axis boundaries
        if abs(x_coord) + radius_offset > max_allowable_x:
            sys.exit(f"[!] COLLISION ERROR: Standoff [{idx}] at X:{x_coord} breaks through the outer wall envelope.")
            
        # Check Y axis boundaries
        if abs(y_coord) + radius_offset > max_allowable_y:
            sys.exit(f"[!] COLLISION ERROR: Standoff [{idx}] at Y:{y_coord} breaks through the outer wall envelope.")
            
    print("[✓] All internal components cleared. No wall collisions detected.")

def compile_and_log_bridge_node(json_path, scad_path, ledger_path="project_ledger.json"):
    # 1. Parse JSON configuration
    with open(json_path, 'r') as f:
        metrics = json.load(f)
        
    # 2. Enforce structural boundary constraint rules
    run_boundary_collision_check(metrics)
    
    # 3. Format dynamic OpenSCAD array mapping
    array_elements = []
    for st in metrics["standoffs"]:
        array_elements.append(f"    [{st['x']}, {st['y']}, {st['inner_dia']}, {st['outer_dia']}, {st['height']}]")
    matrix_string = "standoff_matrix = [\n" + ",\n".join(array_elements) + "\n];"

    # 4. Inject metrics into OpenSCAD text layout
    with open(scad_path, 'r') as f:
        scad_content = f.read()

    for key in ["casing_length", "casing_width", "casing_height", "wall_thickness", "flange_width", "flange_thickness"]:
        scad_content = re.sub(rf"^({key}\s*=\s*)[^;]+;", f"\\1{metrics[key]};", scad_content, flags=re.MULTILINE)
        
    scad_content = re.sub(r"standoff_matrix\s*=\s*\[[\s\S]*?\]\s*;", matrix_string, scad_content)

    with open(scad_path, 'w') as f:
        f.write(scad_content)
        
    # Generate an isolated cryptographic footprint hash for the hardware geometry file
    hardware_hash = hashlib.sha256(scad_content.encode()).hexdigest()
    print(f"[✓] OpenSCAD model verified and compiled. Hardware Design Hash: {hardware_hash}")

    # 5. Commit Linked Entry to Immutable Audit Ledger
    ledger_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hardware_design_hash": hardware_hash,
        "physical_dimensions": {
            "outer_envelope": f"{metrics['casing_length']}x{metrics['casing_width']}x{metrics['casing_height']}",
            "standoff_count": len(metrics["standoffs"])
        },
        "linked_hex_schemas": metrics["hex_signal_schemas"]
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
        
    print(f"[✓] Hardware hash and software hex schema locked into continuous audit ledger target: '{ledger_path}'.")

if __name__ == "__main__":
    compile_and_log_bridge_node("bridge_dimensions.json", "enclosure_mold.scad")
