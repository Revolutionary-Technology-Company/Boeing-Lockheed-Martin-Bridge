if __name__ == "__main__":
    # 1. Compile physical geometry matrix and log structural configurations
    compile_and_log_bridge_node("bridge_dimensions.json", "enclosure_mold.scad")
    
    # 2. Re-render scannable system tracking markdown table for deployment tracking
    generate_markdown_tracking_ledger("project_ledger.json", "TRACKING_LEDGER.md")
