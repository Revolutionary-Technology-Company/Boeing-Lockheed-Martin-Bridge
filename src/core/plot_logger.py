import os
import time
import matplotlib.pyplot as plt

class MatplotlibPlotLogger:
    """
    Automates document auditing by saving real-time airframe geometry alignment 
    plots directly to the project's documentation subdirectories.
    """
    def __init__(self, output_directory: str = "docs/plots"):
        self.output_dir = output_directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def log_figure_to_docs(self, figure: plt.Figure, phase_name: str) -> str:
        """
        Saves the provided active Matplotlib figure object as a clean, high-resolution 
        PNG image artifact inside your repository documentation tree.
        """
        # Generate an isolated, chronological naming string
        timestamp = int(time.time())
        sanitized_phase = phase_name.lower().replace(" ", "_")
        filename = f"alignment_{sanitized_phase}_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        # Save the figure with cropped background bounding parameters
        figure.savefig(
            filepath, 
            dpi=150, 
            facecolor=figure.get_facecolor(), 
            edgecolor='none',
            bbox_inches='tight'
        )
        return filepath
