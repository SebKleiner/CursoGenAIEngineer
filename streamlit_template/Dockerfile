# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
