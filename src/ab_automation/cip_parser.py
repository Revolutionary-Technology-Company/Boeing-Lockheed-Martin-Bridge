import struct

class AllenBradleyCipParser:
    """
    Decodes EtherNet/IP and CIP (Common Industrial Protocol) tag messaging packets
    standardized by Rockwell Automation for Allen-Bradley industrial control hardware.
    """
    def __init__(self):
        self.origin_signature = "ALLEN_BRADLEY"
        # Standard CIP Data Type Codes
        self.CIP_TYPES = {
            0xC1: "BOOL",
            0xC4: "DINT",   # 32-bit signed integer
            0xCA: "REAL"    # 32-bit floating point
        }

    def parse_cip_read_tag_response(self, raw_buffer: bytes) -> dict:
        """
        Parses a raw EtherNet/IP CIP read tag service response packet buffer.
        Extracts structural status, data type, and the corresponding telemetry matrix values.
        """
        if len(raw_buffer) < 4:
            raise ValueError("Buffer underflow: Invalid or truncated CIP message payload.")

        # Byte 0: CIP Service Code (e.g., 0xCC for Read Tag Service Response)
        # Byte 1: Reserved / General Status (0x00 indicates absolute success)
        # Bytes 2-3: CIP Data Type Word
        service_code, general_status, type_word = struct.unpack("<BBH", raw_buffer[:4])
        
        if general_status != 0x00:
            return {
                "origin": self.origin_signature,
                "status": "CIP_ERROR",
                "error_code": hex(general_status).upper(),
                "structural_conformity": False
            }

        data_payload = raw_buffer[4:]
        parsed_value = None

        # Dynamically unpack based on explicit Allen-Bradley hardware data types
        if type_word == 0xC4 and len(data_payload) >= 4:  # DINT
            parsed_value = struct.unpack("<i", data_payload[:4])[0]
        elif type_word == 0xCA and len(data_payload) >= 4:  # REAL
            parsed_value = struct.unpack("<f", data_payload[:4])[0]
        elif type_word == 0xC1 and len(data_payload) >= 1:  # BOOL
            parsed_value = bool(data_payload[0])

        return {
            "origin": self.origin_signature,
            "status": "NOMINAL",
            "service_code": hex(service_code).upper(),
            "ab_data_type": self.CIP_TYPES.get(type_word, f"UNKNOWN_{hex(type_word)}"),
            "decoded_value": parsed_value,
            "telemetry_matrix_hex": data_payload.hex().upper(),
            "structural_conformity": True
        }
