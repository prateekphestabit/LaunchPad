FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API code
COPY api.py .

# Create models directory for volume mount
RUN mkdir -p /app/models

# Set the model path environment variable
ENV MODEL_PATH=/app/models/best_model.pkl

# Expose port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
