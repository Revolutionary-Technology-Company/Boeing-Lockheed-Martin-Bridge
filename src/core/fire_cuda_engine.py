import numpy as np
from numba import cuda

@cuda.jit
def evaluate_bridge_thermal_matrix_kernel(data_matrix, threshold, output_flags):
    """
    Native NVIDIA GPU CUDA kernel executing massive parallel array filtering.
    Bypasses traditional garbage collection bottlenecks to track real-time thermal spikes.
    """
    # Locate unique coordinates across the active 2D GPU execution block
    x, y = cuda.grid(2)
    
    # Check boundaries against the incoming array dimensions
    if x < data_matrix.shape[0] and y < data_matrix.shape[1]:
        val = data_matrix[x, y]
        
        # If any component point breaches safe multi-party engineering limits, flag instantly
        if val > threshold:
            # Atomic operation ensures thread-safe allocation across massive concurrency
            cuda.atomic.max(output_flags, 0, 1)

class FireWatchCudaEngine:
    """
    Primary GPU-bound analytics core mapping structural bridge matrices 
    straight to native CUDA threads for fast spatial-temporal filtering.
    """
    def __init__(self, target_threshold: float = 180.0):
        self.threshold = target_threshold
        self.origin_signature = "FIREWATCH_CUDA_ENGINE"
        self.voltage_steps = np.linspace(0.0, 1.0, 16)

    def evaluate_array_on_gpu(self, structural_matrix: np.ndarray) -> dict:
        """Allocates memory blocks, pushes data onto the GPU, and evaluates flags."""
        if structural_matrix.ndim != 2:
            raise ValueError("Invalid array shape: Expected a flat 2D matrix structure.")
            
        # Ensure array data type matches floating-point float32 specifications
        float_matrix = structural_matrix.astype(np.float32)
        
        # Initialize a 1-element flag matrix directly on the host device
        output_flags_host = np.zeros(1, dtype=np.int32)
        
        # Allocate device memory and stream memory buffers seamlessly to the GPU
        d_matrix = cuda.to_device(float_matrix)
        d_flags = cuda.to_device(output_flags_host)
        
        # Configure optimum 16x16 GPU processing blocks layout
        threads_per_block = (16, 16)
        blocks_per_grid_x = int(np.ceil(float_matrix.shape[0] / 16))
        blocks_per_grid_y = int(np.ceil(float_matrix.shape[1] / 16))
        blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
        
        # Fire the hardware-accelerated parallel computing kernel
        evaluate_bridge_thermal_matrix_kernel[blocks_per_grid, threads_per_block](d_matrix, self.threshold, d_flags)
        
        # Read results back from the GPU memory partition
        output_flags_host = d_flags.copy_to_host()
        anomaly_detected = bool(output_flags_host[0] == 1)
        
        if anomaly_detected:
            status = "CRITICAL_THERMAL_SURGE"
            ui_color = "EMERGENCY_RED"
            voltage_output = 1.0
        else:
            status = "NOMINAL_STABLE"
            ui_color = "NOMINAL_GREEN"
            voltage_output = 0.5

        closest_idx = (np.abs(self.voltage_steps - voltage_output)).argmin()
        hex_voltage_state = hex(closest_idx)[2:].upper()

        return {
            "origin": self.origin_signature,
            "incident_verification": status,
            "hex_voltage_state": f"0.{hex_voltage_state}V",
            "ui_node_color": ui_color,
            "structural_conformity": not anomaly_detected
        }
