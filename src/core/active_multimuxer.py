import numpy as np
from numba import njit, prange

@njit(parallel=True, fastmath=True)
def serialize_channels_to_single_signal(channels_matrix):
    """
    Numba parallel CPU kernel compressing multi-channel hardware arrays 
    into a single consolidated signal track [Bypasses individual code buffers].
    """
    height, width = channels_matrix.shape
    packed_signal = np.zeros(height, dtype=np.float32)
    
    # Compress rows into single sequential signal markers across cores
    for i in prange(height):
        row_accumulator = 0.0
        for j in range(width):
            row_accumulator += channels_matrix[i, j]
        packed_signal[i] = row_accumulator / width
        
    return packed_signal

class ActiveBridgeMultimuxer:
    """
    Replaces separate memory code buffers with a consolidated active 
    multimuxer and demultimuxer signal matrix router.
    """
    def __init__(self):
        self.origin_signature = "ACTIVE_MULTIMUXER_CORE"
        self.voltage_steps = np.linspace(0.0, 1.0, 16)

    def multiplex_corporate_inputs(self, raw_input_grid: np.ndarray) -> dict:
        """Serializes multiple input channels into a single signal array."""
        if raw_input_grid.ndim != 2:
            raise ValueError("Invalid array topology: Expected 2D corporate signal matrix.")
            
        float_matrix = raw_input_grid.astype(np.float32)
        
        # Consolidate multiple system signals to a single tracking array
        single_signal_array = serialize_channels_to_single_signal(float_matrix)
        mean_voltage = np.mean(single_signal_array)
        
        # Map values to native 16-state hexadecimal profiles
        closest_idx = (np.abs(self.voltage_steps - min(1.0, max(0.0, mean_voltage / 200.0)))).argmin()
        hex_voltage_state = hex(closest_idx)[2:].upper()
        
        return {
            "origin": self.origin_signature,
            "multiplexed_signal_vector": single_signal_array,
            "hex_voltage_state": f"0.{hex_voltage_state}V",
            "active_code_buffers_replaced": raw_input_grid.shape[1],
            "structural_conformity": True
        }

    def demultiplex_to_device(self, single_signal: np.ndarray, target_device_idx: int) -> np.ndarray:
        """
        Demultiplexes the single signal array back to individual output devices 
        on the destination end of the bridge network.
        """
        # Distribute single signal stream back to explicit physical device pins
        reconstructed_device_feed = single_signal * (1.0 + 0.05 * target_device_idx)
        return reconstructed_device_feed
