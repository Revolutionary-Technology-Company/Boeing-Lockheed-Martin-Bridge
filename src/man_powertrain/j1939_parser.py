import struct

class ManJ1939CanParser:
    """
    Decodes heavy-duty MAN industrial and marine CAN Bus matrices 
    operating over standard SAE J1939 signaling topologies.
    """
    def __init__(self):
        self.origin_signature = "MAN_INDUSTRIAL"

    def decode_j1939_frame(self, extended_can_id: int, raw_payload: bytes) -> dict:
        """
        Parses a 29-bit J1939 identification matrix to isolate the Priority,
        Parameter Group Number (PGN), and Source Address, then unpacks the data fields.
        """
        if len(raw_payload) < 8:
            raw_payload = raw_payload.ljust(8, b'\xFF') # J1939 default padding character is 0xFF

        # 29-bit ID Breakdown:
        # Bits 0-7: Source Address (SA)
        # Bits 8-25: Parameter Group Number (PGN)
        # Bits 26-28: Priority
        source_address = extended_can_id & 0xFF
        pgn = (extended_can_id >> 8) & 0x3FFFF
        priority = (extended_can_id >> 26) & 0x7

        # Unpack standard 8-byte J1939 word configurations (e.g., 4 structural shorts)
        spn_word_1, spn_word_2, spn_word_3, spn_word_4 = struct.unpack("<HHHH", raw_payload[:8])

        return {
            "origin": self.origin_signature,
            "priority": priority,
            "parameter_group_number": pgn,
            "source_address": hex(source_address).upper(),
            "decoded_spn_matrix": [spn_word_1, spn_word_2, spn_word_3, spn_word_4],
            "telemetry_matrix_hex": raw_payload.hex().upper(),
            "structural_conformity": True
        }
