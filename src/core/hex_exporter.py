import struct
import os

class HexFormatExporter:
    """
    Handles data persistence for the 16-state hexadecimal voltage core.
    Supports raw binary fragment packing and human-readable audit tables.
    """
    def __init__(self, output_dir: str = "docs/hardware_logs"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def save_as_binary_fragment(self, filename: str, hex_string: str) -> str:
        """
        Converts human-readable hex back to raw packed bytes for direct memory 
        injection into legacy hardware without binary translation overhead.
        """
        filepath = os.path.join(self.output_dir, f"{filename}.bin")
        # Ensure strings are even-lengthened for byte conversion
        if len(hex_string) % 2 != 0:
            hex_string += "0"
            
        byte_data = bytes.fromhex(hex_string)
        with open(filepath, "wb") as f:
            f.write(byte_data)
        return filepath

    def save_as_readable_table(self, filename: str, hex_string: str, columns: int = 16) -> str:
        """
        Formats raw hex data into a structural table matrix with memory offset addresses 
        for system engineers to audit manually.
        """
        filepath = os.path.join(self.output_dir, f"{filename}.hex")
        with open(filepath, "w") as f:
            f.write(f"--- UNIVAC IX HARWARE FORENSICS MATRIX [{filename.upper()}] ---\n")
            f.write("Offset(h)  " + " ".join([f"{i:02X}" for i in range(columns)]) + "\n")
            f.write("-" * (12 + (columns * 3)) + "\n")
            
            # Subdivide string into fixed chunk arrays matching table layout rows
            for offset in range(0, len(hex_string), columns * 2):
                chunk = hex_string[offset : offset + (columns * 2)]
                # Group characters into distinct 2-character hex pairs
                pairs = [chunk[i:i+2] for i in range(0, len(chunk), 2)]
                formatted_row = " ".join(pairs)
                
                memory_address = f"{offset // 2:08X}"
                f.write(f"{memory_address}  {formatted_row}\n")
                
        return filepath
