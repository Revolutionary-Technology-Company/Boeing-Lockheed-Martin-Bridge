import numpy as np
from numba import cuda, njit, prange

# ============================================================================
# PIPELINE A: NATIVE NVIDIA GPU CUDA KERNEL (MASSIVE PARALLEL THREADS)
# ============================================================================
@cuda.jit
def evaluate_bridge_thermal_matrix_kernel(data_matrix, threshold, output_flags):
    """
    NVIDIA GPU CUDA execution block. Maps matrix coordinates directly to hardware 
    GPU streaming multiprocessor warp tracks for zero-overhead validation.
    """
    x, y = cuda.grid(2)
    if x < data_matrix.shape[0] and y < data_matrix.shape[1]:
        if data_matrix[x, y] > threshold:
            cuda.atomic.max(output_flags, 0, 1)

# ============================================================================
# PIPELINE B: MULTI-CORE CPU JIT ENGINE (AUTOMATED MULTI-THREAD RUNTIME)
# ============================================================================
@njit(parallel=True, fastmath=True)
def fallback_multicore_cpu_analysis(data_matrix, threshold):
    """
    High-performance fallback CPU loop. Forces parallel work-sharing schedules
    across all physical multi-core threads using openmp/tbb.
    """
    height, width = data_matrix.shape
    breach_count = 0
    
    # prange explicitly distribution steps across all available machine hardware cores
    for i in prange(height):
        for j in range(width):
            if data_matrix[i, j] > threshold:
                breach_count += 1
                
    return breach_count > 0

# ============================================================================
# HARDWARE CONTROLLER CORE
# ============================================================================
class FireWatchHardwareEngine:
    """
    Orchestrates twin-engine acceleration properties to track real-time 
    structural anomalies over Boeing-Lockheed Martin data streams.
    """
    def __init__(self, target_threshold: float = 180.0):
        self.threshold = target_threshold
        self.voltage_steps = np.linspace(0.0, 1.0, 16)

    def process_matrix_frame(self, structural_matrix: np.ndarray, force_cpu: bool = False) -> dict:
        float_matrix = structural_matrix.astype(np.float32)
        anomaly_detected = False
        execution_engine = "UNKNOWN"

        # Check for active local NVIDIA hardware driver connectivity links
        if cuda.is_available() and not force_cpu:
            execution_engine = "NVIDIA_GPU_CUDA"
            output_flags_host = np.zeros(1, dtype=np.int32)
            
            # Map memory spaces straight to unmanaged GPU hardware blocks
            d_matrix = cuda.to_device(float_matrix)
            d_flags = cuda.to_device(output_flags_host)
            
            threads_per_block = (16, 16)
            blocks_x = int(np.ceil(float_matrix.shape[0] / 16))
            blocks_y = int(np.ceil(float_matrix.shape[1] / 16))
            
            # Trigger native GPU warp pipeline execution steps
            evaluate_bridge_thermal_matrix_kernel[(blocks_x, blocks_y), threads_per_block](d_matrix, self.threshold, d_flags)
            output_flags_host = d_flags.copy_to_host()
            anomaly_detected = bool(output_flags_host[0] == 1)
        else:
            # Fallback seamlessly into high-throughput Multi-Core CPU routines
            execution_engine = "MULTICORE_PARALLEL_CPU"
            anomaly_detected = fallback_multicore_cpu_analysis(float_matrix, self.threshold)

        if anomaly_detected:
            status = "CRITICAL_THERMAL_SURGE"
            voltage_output = 1.0
        else:
            status = "NOMINAL_STABLE"
            voltage_output = 0.5

        closest_idx = (np.abs(self.voltage_steps - voltage_output)).argmin()
        hex_voltage_state = hex(closest_idx)[2:].upper()

        return {
            "active_hardware_engine": execution_engine,
            "incident_verification": status,
            "hex_voltage_state": f"0.{hex_voltage_state}V",
            "structural_conformity": not anomaly_detected
        }
