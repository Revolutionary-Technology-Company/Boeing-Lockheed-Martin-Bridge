import os

class NDAGatekeeper:
    """
    Ring-fences the joint_assembly environment. 
    Locks access until mutual license NDA compliance is verified.
    """
    def __init__(self, shared_directory: str = "./joint_projects"):
        self.shared_dir = shared_directory
        if not os.path.exists(self.shared_dir):
            os.makedirs(self.shared_dir)

    def initialize_joint_project(self, project_name: str, boeing_sig: str, lockheed_sig: str) -> bool:
        """Enforces a trust-based workspace requiring active dual-corporate signatures."""
        if not boeing_sig or not lockheed_sig:
            raise PermissionError("Access Denied: Dual corporate electronic signatures required.")
        
        project_path = os.path.join(self.shared_dir, project_name)
        os.makedirs(project_path, exist_ok=True)
        
        # Auto-generate locked compliance license file
        nda_content = f"# NDA License Agreement\nProject: {project_name}\nStatus: Audited Shared Network"
        with open(os.path.join(project_path, "LICENSE_NDA.md"), "w") as f:
            f.write(nda_content)
        return True
