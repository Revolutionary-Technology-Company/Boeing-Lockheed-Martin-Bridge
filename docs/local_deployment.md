# 1. Activate your virtual terminal context
source venv/bin/activate

# 2. Ingest your new package definitions cleanly
pip install -r requirements.txt

# 3. Verify the electrostatic safety layers evaluate successfully
pytest tests/test_discharge_logic.py
