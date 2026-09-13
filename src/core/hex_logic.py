import numpy as np

class HexadecimalVoltageMatrix:
    """
    Handles native 16-state analog logic matrices over 0.0V to 1.0V voltage intervals.
    Bypasses traditional binary processing bottlenecks.
    """
    def __init__(self):
        # 16 distinct voltage intervals stepping by 0.0625V
        self.voltage_steps = np.linspace(0.0, 1.0, 16)
        
    def decode_signal(self, voltage_reading: float) -> str:
        """Maps a physical voltage directly to its corresponding hex character state."""
        closest_idx = (np.abs(self.voltage_steps - voltage_reading)).argmin()
        return hex(closest_idx)[2:].upper()

    def process_telemetry_stream(self, stream: list) -> str:
        """Processes raw analog stream matrices directly into hardware forensics."""
        return "".join([self.decode_signal(v) for v in stream])
