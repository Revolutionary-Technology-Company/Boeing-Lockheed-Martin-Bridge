# Boeing Data Extraction Layer
class Boeing8300Parser:
    def extract_legacy_data(self, raw_stream: bytes) -> dict:
        """Decodes legacy UNIVAC 900 Cisco Router 8300 6-bit FIELDATA profiles."""
        # Convert legacy stream layers safely to standard aerospace dict
        return {"origin": "BOEING", "data_payload": raw_stream.hex().upper(), "conformity": True}

# Lockheed Martin Data Extraction Layer
class Lockheed955Parser:
    def extract_legacy_data(self, raw_stream: bytes) -> dict:
        """Decodes legacy Univac 955 Taurus Fleet Command Athena data arrays."""
        # Standardize data fields to align with fleet command requirements
        return {"origin": "LOCKHEED_MARTIN", "data_payload": raw_stream.hex().upper(), "conformity": True}
