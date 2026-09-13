import unittest
import json
import re

class TestUnivacHexSignals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the centralized parameter file containing the hex schemas
        with open("bridge_dimensions.json", "r") as f:
            cls.config = json.load(f)
        cls.schemas = cls.config["hex_signal_schemas"]

    def verify_signal_payload(self, raw_hex_string, schema_key):
        """Helper to match raw hex inputs against expected schema boundaries."""
        schema = self.schemas[schema_key]
        header = schema["header_sig"]
        trailer = schema["trailer_sig"]
        
        # Build pattern: Must start with header signature and end with trailer signature
        pattern = rf"^{header}([0-9A-FA-f]*){trailer}$"
        match = re.match(pattern, raw_hex_string.upper())
        
        if not match:
            return False, "Malformed packet: Header/Trailer frame mismatch or invalid hex character."
            
        payload_data = match.group(1)
        return True, payload_data

    def test_boeing_univac_900_valid_signal(self):
        """Verifies a correct Boeing-aligned raw hex payload."""
        # Frame: Header (4E5558393030) + Dummy Data (AABBCCDD) + Trailer (454E44)
        valid_boeing_packet = "4E5558393030AABBCCDD454E44"
        success, message = self.verify_signal_payload(valid_boeing_packet, "UNIVAC_900_BOEING")
        self.assertTrue(success, msg=message)
        self.assertEqual(message, "AABBCCDD")

    def test_lockheed_univac_955_valid_signal(self):
        """Verifies a correct Lockheed-aligned raw hex payload."""
        # Frame: Header (544155525553) + Dummy Data (FFEE1122) + Trailer (454E44)
        valid_lockheed_packet = "544155525553FFEE1122454E44"
        success, message = self.verify_signal_payload(valid_lockheed_packet, "UNIVAC_955_LOCKHEED")
        self.assertTrue(success, msg=message)

    def test_invalid_packet_rejection(self):
        """Enforces strict rejection of corrupt frames or alignment errors."""
        corrupt_packet = "4E5558393030CORRUPTDATA454E44" # Contains non-hex chars
        success, _ = self.verify_signal_payload(corrupt_packet, "UNIVAC_900_BOEING")
        self.assertFalse(success, "The test should have rejected non-hexadecimal data.")

if __name__ == "__main__":
    unittest.main()
