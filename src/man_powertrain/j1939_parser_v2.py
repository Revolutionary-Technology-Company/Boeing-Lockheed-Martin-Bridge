import struct

class ManSurfacePanelsParser:
    """
    Decodes heavy industrial MAN surface manufacturing matrices and skin panel
    telemetry arrays operating over standard SAE J1939 signaling topologies.
    """
    def __init__(self):
        self.origin_signature = "MAN_SURFACES"

    def decode_panel_geometry_frame(self, extended_can_id: int, raw_payload: bytes) -> dict:
        """
        Parses a 29-bit J1939 structural identity matrix to track external panels.
        Isolates the Parameter Group Number (PGN) and unpacks surface deflection millimetric floats.
        """
        if len(raw_payload) < 8:
            raw_payload = raw_payload.ljust(8, b'\xFF')

        # J1939 Arbitration Matrix Breakdown
        source_address = extended_can_id & 0xFF
        pgn = (extended_can_id >> 8) & 0x3FFFF
        priority = (extended_can_id >> 26) & 0x7

        # Unpack 8-byte payload representing 4 high-precision millimetric alignment variables
        # Maps surface planar displacement, contour angles, and edge latch tolerances
        surface_delta_x, surface_delta_y, edge_gap, shear_strain = struct.unpack("<hhhh", raw_payload[:8])

        # Scale raw short integers to true physical engineering dimensions (e.g., 0.001mm scale multiplier)
        return {
            "origin": self.origin_signature,
            "priority": priority,
            "parameter_group_number": pgn,
            "source_address": hex(source_address).upper(),
            "surface_metrics": {
                "planar_displacement_x_mm": surface_delta_x * 0.001,
                "planar_displacement_y_mm": surface_delta_y * 0.001,
                "panel_edge_gap_mm": edge_gap * 0.001,
                "skin_shear_strain_microstrain": float(shear_strain)
            },
            "telemetry_matrix_hex": raw_payload.hex().upper(),
            "structural_conformity": True
        }
