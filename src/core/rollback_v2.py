import os
import shutil
import struct
import requests
from core.autocad_bridge import AutoCADProductBridge

class CadAutomatedRollbackEngine:
    """
    Automated system state restore engine. Reverts local cluster vector formats
    and dispatches a CCSDS emergency Safe-Stop command packet to NASA cFS endpoints.
    """
    def __init__(self, workspace_directory: str = "./joint_projects", crypto_key: str = None):
        self.workspace_dir = workspace_directory
        self.bridge = AutoCADProductBridge(workspace_directory, crypto_key)
        self.backup_dir = os.path.join(self.workspace_dir, ".stable_backups")
        self.nasa_command_gateway = "https://nasa.gov"
        
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def _dispatch_nasa_safestop_packet(self) -> bool:
        """
        Compiles and posts a mandatory 6-byte binary CCSDS Emergency Command Packet.
        Targeting APID: 0x180 (Emergency Stop App) with a sequential sequence count.
        """
        # CCSDS Header Packing Layout:
        # Word 1: 0x1980 (Version 0, Cmd Type 1, Sec Header 1, APID 0x180)
        # Word 2: 0xC000 (Sequence Flags 0b11 [Unsegmented], Sequence Count 0)
        # Word 3: 0x0001 (Command Payload Length - 1 = 1 byte of verification data)
        ccsds_cmd_header = struct.pack(">HHH", 0x1980, 0xC000, 0x0001)
        verification_payload = b'\xAA'  # Hard emergency verification byte code
        full_packet = ccsds_cmd_header + verification_payload

        try:
            response = requests.post(
                self.nasa_command_gateway, 
                data=full_packet, 
                headers={"Content-Type": "application/octet-stream"},
                timeout=2.0
            )
            return response.status_code == 200
        except requests.RequestException:
            # Non-blocking fallback alert log for local telemetry tracking
            print("[-] Warning: Direct NASA Command network gateway link unavailable.")
            return False

    def execute_emergency_rollback(self, target_filename: str) -> bool:
        """Restores the active layout, locks files, and alerts NASA immediately."""
        backup_path = os.path.join(self.backup_dir, f"stable_{target_filename}")
        active_path = os.path.join(self.workspace_dir, target_filename)

        if not os.path.exists(backup_path):
            return False

        # 1. Dispatch the primary binary network alert to NASA's cFS pipeline
        self._dispatch_nasa_safestop_packet()
        
        # 2. Restore local physical engineering layouts
        shutil.copy2(backup_path, active_path)
        
        # 3. Encrypt storage blocks and push branch code back to the main repository
        encrypted_artifact = self.bridge.encrypt_production_file(target_filename)
        return self.bridge.commit_and_push_to_main(
            target_filename=os.path.basename(encrypted_artifact),
            commit_message="CRITICAL LOCKOUT: Reverted system vectors and triggered NASA Safe-Stop."
        )
