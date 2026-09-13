import struct

class NorthropGrummanLink16Parser:
    """
    Decodes MIL-STD-6016 Link 16 Tactical Data Link (TADIL) streams,
    unpacking J-Series binary tracking frames utilized by Northrop Grumman platforms.
    """
    def __init__(self):
        self.origin_signature = "NORTHROP_GRUMMAN"

    def parse_j_series_track_packet(self, raw_buffer: bytes) -> dict:
        """
        Parses a raw binary Link 16 J-Series message packet payload.
        Isolates standard tracking labels, platform coordinates, and dimension offsets.
        """
        if len(raw_buffer) < 8:
            raise ValueError("Buffer underflow: Invalid or truncated Link 16 packet data.")

        # Unpack standard MIL-STD-6016 header parameters:
        # Byte 0: Message Label (e.g., 2 indicates J2 Track Message Group)
        # Byte 1: Sublabel / Subfunction (e.g., 2 indicates J2.2 Precise Location Block)
        # Bytes 2-3: Source Track Number identifier word
        # Bytes 4-7: Extracted coordinate dimension scaling integer
        label, sublabel, track_id, raw_coordinate = struct.unpack("<BBHI", raw_buffer[:8])
        
        # Scale coordinates to fit precisely within the 16-state 0.0V-1.0V envelope
        normalized_scalar = (raw_coordinate % 1000) / 1000.0
        
        return {
            "origin": self.origin_signature,
            "link16_label": f"J{label}.{sublabel}",
            "source_track_id": hex(track_id).upper(),
            "scaled_displacement_factor": normalized_scalar,
            "telemetry_matrix_hex": raw_buffer[:8].hex().upper(),
            "structural_conformity": True if label > 0 else False
        }
