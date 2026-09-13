import struct

class NasaCcsdsSpaceParser:
    """
    Decodes Consultative Committee for Space Data Systems (CCSDS) Space Packets
    utilized across NASA cFS (Core Flight System) mission architecture telemetry.
    """
    def __init__(self):
        self.origin_signature = "NASA_OPERATIONS"

    def parse_ccsds_header(self, raw_packet: bytes) -> dict:
        """
        Parses a standard 6-byte CCSDS primary telemetry header block 
        to isolate the tracking APID and sequence constraints.
        """
        if len(raw_packet) < 6:
            raise ValueError("Telemetry packet underflow: Missing mandatory 48-bit CCSDS header block.")

        # Unpack structural header bits: 
        # Word 1: Version (3 bits), Packet Type (1 bit), Sec Header Flag (1 bit), APID (11 bits)
        # Word 2: Sequence Flags (2 bits), Sequence Count (14 bits)
        # Word 3: Packet Data Length (16 bits)
        word_1, word_2, packet_len = struct.unpack(">HHH", raw_packet[:6])
        
        apid = word_1 & 0x07FF
        sequence_count = word_2 & 0x3FFF
        true_data_length = packet_len + 1  # CCSDS length parameter definition specifies length - 1
        
        return {
            "origin": self.origin_signature,
            "application_process_id_apid": apid,
            "packet_sequence_count": sequence_count,
            "payload_data_length_bytes": true_data_length,
            "structural_conformity": True if apid > 0 else False
        }
