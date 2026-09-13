# 1. Activate your core environment shell
source venv/bin/activate

# 2. Re-install all updated package definitions cleanly
pip install -r requirements.txt

# 3. Execute the automated regression tests to verify industrial compatibility
pytest
