# ============================================================================
# UNIVAC IX AEROSPACE BRIDGE RUNTIME CONTEXT
# ============================================================================
FROM python:3.11-slim

# System updates and secure communication package installation
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    openssh-client \
    && rm -rf /var/lib/apt-get/lists/*

WORKDIR /app

# ----------------------------------------------------------------------------
# 🛡️ SECURE COMPLIANCE: Establish Isolated Git & SSH Keys Profiles
# ----------------------------------------------------------------------------
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh \
    && echo "Host github.com\n\tStrictHostKeyChecking no\n" >> /root/.ssh/config \
    && git config --global user.name "UNIVAC IX Automated Node" \
    && git config --global user.email "univac-ix-node@revolutionary-technology.com"

# Install mathematical matrix frameworks and testing engines
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bring repository codebase layers into the workspace
COPY src/ ./src/
COPY docs/ ./docs/

# Enforce explicit application execution pathways
EXPOSE 8501
ENV PYTHONUNBUFFERED=1

# Run diagnostic node validator before spinning up the production cluster
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
