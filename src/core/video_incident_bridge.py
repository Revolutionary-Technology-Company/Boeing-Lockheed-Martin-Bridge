import numpy as np
from numba import njit, prange

@njit(parallel=True, fastmath=True)
def analyze_unmanaged_pixel_matrix(frame_buffer: np.ndarray, threshold_intensity: float) -> float:
    """
    Accelerated parallel CPU kernel using Numba NJIT to crunch 
    unmanaged video frame pixel matrices.
    Tracks raw intensity signatures to verify emergency visual flare events.
    """
    height, width, channels = frame_buffer.shape
    total_pixels = height * width
    intensity_accumulator = 0.0
    
    # Execute flat parallelized loop structures across pixel arrays
    for i in prange(height):
        for j in range(width):
            # Isolate raw red-channel bias and luminance signatures
            r_val = frame_buffer[i, j, 0]
            g_val = frame_buffer[i, j, 1]
            b_val = frame_buffer[i, j, 2]
            
            # Simplified high-speed luminance computation model
            luminance = 0.299 * r_val + 0.587 * g_val + 0.114 * b_val
            if luminance > threshold_intensity and r_val > (g_val * 1.5):
                intensity_accumulator += 1.0
                
    return intensity_accumulator / total_pixels

class GenetecEdwardsIncidentBridge:
    """
    Middleware bridge linking Genetec Security Center live video matrices 
    with Edwards FireWorks Incident Platform notification channels.
    """
    def __init__(self, incident_trigger_ratio: float = 0.05):
        self.trigger_ratio = incident_trigger_ratio
        self.origin_signature = "HYPER_TOMCAT_BRIDGE"
        self.voltage_steps = np.linspace(0.0, 1.0, 16)

    def process_live_stream_frame(self, raw_frame: np.ndarray, active_threshold: float = 200.0) -> dict:
        """Processes a frame matrix through the parallelized core analysis loop."""
        if raw_frame.ndim != 3:
            raise ValueError("Invalid frame dimensions: Expected a 3D [H x W x C] pixel array.")
            
        # Run the compiled JIT execution routine
        anomaly_ratio = analyze_unmanaged_pixel_matrix(raw_frame, active_threshold)
        
        # Check against strict trigger margins to verify live incident threats
        if anomaly_ratio >= self.trigger_ratio:
            incident_status = "CRITICAL_ANOMALY"
            ui_node_color = "EMERGENCY_RED"
        else:
            incident_status = "NOMINAL_STABLE"
            ui_node_color = "NOMINAL_GREEN"
            
        # Map structural ratio values to native 16-state hexadecimal voltage levels
        closest_idx = (np.abs(self.voltage_steps - min(1.0, anomaly_ratio * 10))).argmin()
        hex_voltage_state = hex(closest_idx)[2:].upper()
            
        return {
            "origin": self.origin_signature,
            "incident_verification": incident_status,
            "visual_anomaly_ratio": anomaly_ratio,
            "hex_voltage_state": f"0.{hex_voltage_state}V",
            "ui_node_color": ui_node_color
        }
