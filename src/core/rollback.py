import os
import shutil
from core.autocad_bridge import AutoCADProductBridge

class CadAutomatedRollbackEngine:
    """
    Automated system state restore engine. Catches critical infrastructure faults 
    and instantly reverts the cluster configuration to the last known stable layout.
    """
    def __init__(self, workspace_directory: str = "./joint_projects", crypto_key: str = None):
        self.workspace_dir = workspace_directory
        self.bridge = AutoCADProductBridge(workspace_directory, crypto_key)
        self.backup_dir = os.path.join(self.workspace_dir, ".stable_backups")
        
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def checkpoint_current_stable_state(self, filename: str) -> str:
        """Saves a verified, working engineering snapshot to the local cache directory."""
        source_path = os.path.join(self.workspace_dir, filename)
        backup_path = os.path.join(self.backup_dir, f"stable_{filename}")
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, backup_path)
            return backup_path
        return ""

    def execute_emergency_rollback(self, target_filename: str) -> bool:
        """
        Restores the active design environment to the cached stable configuration, 
        re-encrypts files, and synchronization-pushes the safe layout to the main branch.
        """
        backup_name = f"stable_{target_filename}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        active_path = os.path.join(self.workspace_dir, target_filename)

        if not os.path.exists(backup_path):
            print(f"[-] Rollback aborted: No stable hardware state cached for {target_filename}")
            return False

        print(f"[!] FAULT ENCOUNTERED: Restoring physical matrix to {backup_name}...")
        
        # 1. Restore the working drawing text file from the safe cache
        shutil.copy2(backup_path, active_path)
        
        # 2. Re-encrypt the restored layout to protect corporate IP
        encrypted_artifact = self.bridge.encrypt_production_file(target_filename)
        enc_filename = os.path.basename(encrypted_artifact)

        # 3. Force-sync the safe layout change back up to your active working repository
        pushed = self.bridge.commit_and_push_to_main(
            target_filename=enc_filename,
            commit_message="EMERGENCY ROLLBACK: Reverted airframe parameters to last known nominal state."
        )
        return pushed
