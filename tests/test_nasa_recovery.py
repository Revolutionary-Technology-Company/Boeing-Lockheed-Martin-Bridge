import pytest
import os
import matplotlib.pyplot as plt
from src.core.rollback import CadAutomatedRollbackEngine
from src.core.plot_logger import MatplotlibPlotLogger

def test_matplotlib_logger_io(tmpdir):
    # Setup temporary docs directory wrapper
    logger = MatplotlibPlotLogger(output_directory=str(tmpdir))
    
    # Construct a basic dummy plotting model
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    
    saved_file = logger.log_figure_to_docs(fig, phase_name="Unit_Test_Phase")
    
    assert os.path.exists(saved_file)
    assert saved_file.endswith(".png")
    plt.close(fig)
