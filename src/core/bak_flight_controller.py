import numpy as np

class SaiyaFlightController:
    """
    Manages omnidirectional maneuverability loops for the Type-S platform.
    Shifts the charge density across a 360-degree plate array to rotate the
    asymmetric repulsion vector without traditional mechanical control surfaces.
    """
    def __init__(self, target_hover_charge: float = 98.0):
        self.base_charge = target_hover_charge
        self.total_plates = 360

    def compute_steering_matrix(self, target_heading_degrees: float, maneuver_intensity: float) -> np.ndarray:
        """
        Calculates an array containing the exact Coulomb saturation level for each 
        of the 360 plates to bias the repulsion vector toward a target angle.
        """
        # Initialize a flat base charge array across all 360 segments (unbiased hover)
        plate_matrix = np.full(self.total_plates, self.base_charge / self.total_plates)
        
        # Convert degrees to target plate indexing steps
        target_idx = int(target_heading_degrees % 360)
        
        # Apply a smooth sinusoidal bias distribution loop across the array
        for plate_idx in range(self.total_plates):
            angular_distance = np.radians(plate_idx - target_idx)
            # Leading edge gains charge saturation, trailing edge sheds charge saturation
            bias = maneuver_intensity * np.cos(angular_distance)
            plate_matrix[plate_idx] = max(0.0, plate_matrix[plate_idx] + bias)
            
        return plate_matrix
