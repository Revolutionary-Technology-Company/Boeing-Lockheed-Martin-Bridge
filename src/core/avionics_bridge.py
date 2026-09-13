import numpy as np

class HyperTomcatAvionicsBridge:
    """
    Synthesizes legacy 36-bit military avionics register logic with native
    high-performance computing on the UNIVAC IX Core Fabric.
    """
    def __init__(self):
        # 36-bit masking constants
        self.MASK_36_BIT = 0xFFFFFFFFF
        self.voltage_steps = np.linspace(0.0, 1.0, 16)
        self.origin_signature = "HYPER_TOMCAT_AVIONICS"

    def parse_36bit_word(self, raw_word: int) -> dict:
        """
        Slices a legacy 36-bit data word into separate tracking fields for
        Boeing airframe sensors and Lockheed flight control vectors.
        """
        # Ensure input word is properly bound within 36-bit limits
        sanitized_word = raw_word & self.MASK_36_BIT
        
        # Split word into functional components:
        # Bits 0-11: Boeing Airframe Status (12 bits)
        # Bits 12-23: Lockheed Avionics Vectors (12 bits)
        # Bits 24-35: Weapon / Tactical Configuration (12 bits)
        boeing_status = (sanitized_word) & 0xFFF
        lockheed_vectors = (sanitized_word >> 12) & 0xFFF
        tactical_config = (sanitized_word >> 24) & 0xFFF
        
        # Map values to a normalized 0.0V - 1.0V signal potential
        normalized_voltage = (lockheed_vectors / 4095.0)
        closest_idx = (np.abs(self.voltage_steps - normalized_voltage)).argmin()
        hex_voltage_state = hex(closest_idx)[2:].upper()

        return {
            "origin": self.origin_signature,
            "boeing_airframe_status_field": hex(boeing_status).upper(),
            "lockheed_avionics_vector_field": hex(lockheed_vectors).upper(),
            "tactical_configuration_field": hex(tactical_config).upper(),
            "hex_voltage_state": f"0.{hex_voltage_state}V",
            "structural_conformity": True
        }
