FROM python:3.10-slim

WORKDIR /app

COPY . /app
# Add this line to Dockerfile
COPY data/sqlite/Equity.db /app/data/sqlite/Equity.db

# Upgrade pip to avoid dependency issues
RUN pip install --upgrade pip

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "PYTHONPATH=$(pwd) python frontend/app.py"]