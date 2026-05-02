FROM python:3.11-slim
LABEL authors="maiaungureanu"

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

ENV PYTHONPATH=/app

# Command to run the app
# Using --host 0.0.0.0 is critical so the container can "talk" to your laptop
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]