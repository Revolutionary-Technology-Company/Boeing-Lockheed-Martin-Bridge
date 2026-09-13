import numpy as np

class ACDelcoWiringHarness:
    """
    Simulates an AC Delco automotive-grade wiring electronics interface.
    Maps physical circuit voltage profiles straight into hexadecimal signal matrices.
    """
    def __init__(self, baseline_resistance_ohms: float = 0.25):
        self.wire_resistance = baseline_resistance_ohms
        # 16-state step voltage mapping from 0.0V to 1.0V (0.0625V intervals)
        self.voltage_steps = np.linspace(0.0, 1.0, 16)

    def calculate_voltage_drop(self, current_amps: float, supply_voltage: float = 1.0) -> float:
        """Calculates internal wiring harness drop over 2oz/3oz thick copper paths."""
        drop = current_amps * self.wire_resistance
        return max(0.0, supply_voltage - drop)

    def convert_voltage_to_hex(self, measured_voltage: float) -> str:
        """Converts raw analog pin voltage to native 16-state Hexadecimal logic."""
        closest_idx = (np.abs(self.voltage_steps - measured_voltage)).argmin()
        return hex(closest_idx)[2:].upper()

    def process_wire_bus_telemetry(self, amp_readings: list) -> str:
        """Processes continuous bus current readings into an audited hex telemetry string."""
        hex_out = []
        for amps in amp_readings:
            v_signal = self.calculate_voltage_drop(amps)
            hex_out.append(self.convert_voltage_to_hex(v_signal))
        return "".join(hex_out)
