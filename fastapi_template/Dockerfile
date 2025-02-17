# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code and shared files from the backend directory
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8080

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
