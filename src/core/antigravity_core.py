import numpy as np

class ACDelcoAntigravityEngine:
    """
    Manages charge routing for the 360-segment Type-S Saiya hull array.
    Translates electrostatic lift potentials directly into 0.0V-1.0V hex logic loops.
    """
    def __init__(self, vessel_mass_kg: float = 1000.0):
        self.mass = vessel_mass_kg
        self.earth_field = 100.0  # Earth's average surface electric field (N/C)
        self.voltage_steps = np.linspace(0.0, 1.0, 16)
        
    def calculate_required_hover_charge(self) -> float:
        """Computes the necessary Coulombs required to generate stable hover repulsion."""
        # Fg = m * g | Fe = q * E -> q = (m * g) / E
        required_charge = (self.mass * 9.8) / self.earth_field
        return required_charge  # Evaluates strictly to 98.0 Coulombs for 1 metric ton

    def map_plate_potential_to_hex(self, current_coulombs: float) -> str:
        """Converts raw Coulomb potentials to native hexadecimal analog signals."""
        target_hover = self.calculate_required_hover_charge()
        # Scale current charge state to a normalized 0.0V - 1.0V voltage envelope
        normalized_voltage = min(1.0, max(0.0, current_coulombs / (target_hover * 1.2)))
        closest_idx = (np.abs(self.voltage_steps - normalized_voltage)).argmin()
        return hex(closest_idx)[2:].upper()

    def calculate_asymmetric_vector(self, quadrant_intensities: list) -> str:
        """Processes an array of 4 charge sectors to map trajectory vector shifts."""
        return "".join([self.map_plate_potential_to_hex(q) for q in quadrant_intensities])
