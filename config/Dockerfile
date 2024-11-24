# Use official Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application files into the container
COPY . /app
RUN pip freeze > requirements.txt
# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Dash app
EXPOSE 8050

# Start the app
CMD ["python", "frontend/app.py"]

