import json
import subprocess
import os
import sys
from datetime import datetime

def mint_edtr_administrative_release(ledger_json_path="project_ledger.json"):
    """
    Generates structured Git tags following administrative EDTR schema parameters.
    Format Paradigm: EDTR-v[Major].[Minor].[Build_Index]-[Hardware_Hash_Prefix]
    """
    if not os.path.exists(ledger_json_path):
        sys.exit(f"Error: Unified audit ledger target '{ledger_json_path}' must exist to map a tracking release.")

    with open(ledger_json_path, "r") as f:
        ledger_data = json.load(f)

    if not ledger_data:
        sys.exit("Error: Ledger register contains no valid historical compiles.")

    # Retrieve parameters of the current active compilation frame
    active_entry = ledger_data[-1]
    build_index = len(ledger_data)
    hw_hash_short = active_entry["hardware_design_hash"][:7].upper()
    
    # Apply official EDTR schema formatting parameters
    edtr_tag = f"EDTR-v0.1.{build_index}-{hw_hash_short}"
    release_notes = f"Official Bridge Node Release - Compiled at {active_entry['timestamp']}"

    print(f"[*] Formatting administrative deployment schema tag: {edtr_tag}")

    try:
        # Push tag metadata to local git index structures
        subprocess.run(["git", "tag", "-a", edtr_tag, "-m", release_notes], check=True)
        print(f"[✓] Administrative tag successfully created inside workspace.")
        print(f"[*] Execute 'git push origin {edtr_tag}' to transmit to the trust network root.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Tag generation aborted. Entry may already exist or workspace is locked: {e}")

if __name__ == "__main__":
    mint_edtr_administrative_release()
