import struct
import random
import time

class Link16MessageGenerator:
    """
    Simulates live MIL-STD-6016 Link 16 tactical transmission matrices.
    Generates byte-packed J-Series messages for tracking air target displacements.
    """
    def __init__(self, baseline_track_id: int = 1024):
        self.track_id = baseline_track_id

    def generate_live_j2_packet(self, base_coordinate: float = 500.0) -> bytes:
        """
        Compiles an 8-byte binary Link 16 packet string containing structured track fields.
        
        Packing Layout:
        - Byte 0: 2 (J2 Message Group)
        - Byte 1: 2 (J2.2 Precise Location Function)
        - Bytes 2-3: 16-bit track ID integer
        - Bytes 4-7: 32-bit tracking coordinate displacement with slight random oscillation
        """
        message_label = 2
        sublabel = 2
        
        # Add artificial telemetry skew to simulate real-world physical vibration
        vibration_variance = random.randint(-15, 15)
        simulated_coordinate = int(base_coordinate + vibration_variance)
        
        # Pack to little-endian: 2 Bytes Unsigned Char, 1 Unsigned Short, 1 Unsigned Int
        binary_packet = struct.pack("<BBHI", message_label, sublabel, self.track_id, simulated_coordinate)
        return binary_packet

    def simulate_continuous_tactical_stream(self, cycles: int = 5, interval_sec: float = 0.5):
        """Yields continuous binary transmission bytes down network lines for stress testing."""
        for _ in range(cycles):
            yield self.generate_live_j2_packet()
            time.sleep(interval_sec)
