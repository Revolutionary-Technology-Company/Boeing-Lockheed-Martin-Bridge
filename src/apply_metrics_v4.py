def generate_markdown_tracking_ledger(ledger_json_path="project_ledger.json", output_md_path="TRACKING_LEDGER.md"):
    """
    Parses structural iteration history records and rewrites a clean, scannable
    Markdown tracking ledger table to establish an unalterable history log.
    """
    if not os.path.exists(ledger_json_path):
        print(f"[!] No ledger data found at {ledger_json_path} to render markdown table.")
        return

    with open(ledger_json_path, "r") as f:
        ledger_data = json.load(f)

    # Initialize layout headers
    md_content = [
        "# 📑 Boeing-Lockheed Martin Bridge Node: Tracking Ledger",
        f"*Automated Build Sync Generation — Last Run: {datetime.utcnow().isoformat()}Z*\n",
        "This ledger documents every verified iteration compile across the shared trust-based network. Every hardware envelope update automatically updates this historical audit matrix.\n",
        "| Iteration | Timestamp (UTC) | Hardware Design Footprint Hash | Enclosure Size | Standoffs Count | Linked Hex Schemas |",
        "| :---: | :--- | :--- | :--- | :---: | :--- |"
    ]

    # Dynamically build rows from the project ledger history trace
    for index, entry in enumerate(ledger_data, start=1):
        schemas_tracked = ", ".join(entry["linked_hex_schemas"].keys())
        row = (
            f"| **v0.{index}** | "
            f"`{entry['timestamp']}` | "
            f"`{entry['hardware_design_hash'][:12]}...` | "
            f"{entry['physical_dimensions']['outer_envelope']} | "
            f"{entry['physical_dimensions']['standoff_count']} | "
            f"{schemas_tracked} |"
        )
        md_content.append(row)

    # Output to the project file path target
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content) + "\n")
        
    print(f"[✓] Automated markdown tracking ledger table written to active target: '{output_md_path}'")
