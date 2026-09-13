import json
import re

def update_scad_parameters(json_path, scad_path):
    # Load custom metric definitions
    with open(json_path, 'r') as j_file:
        metrics = json.load(j_file)
    
    # Read the active CAD template code
    with open(scad_path, 'r') as s_file:
        scad_content = s_file.read()
        
    # Programmatically look for default declarations and override them
    for key, value in metrics.items():
        pattern = rf"^({key}\s*=\s*)[^;]+;"
        replacement = f"\\1{value};"
        scad_content = re.sub(pattern, replacement, scad_content, flags=re.MULTILINE)
        
    # Write back the calculated structural template file
    with open(scad_path, 'w') as s_file:
        s_file.write(scad_content)
        
    print(f"[✓] Automated build pipeline sync complete. Enclosure metrics updated via '{json_path}'.")

if __name__ == "__main__":
    update_scad_parameters("bridge_dimensions.json", "enclosure_mold.scad")
