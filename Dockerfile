# Use an official Python runtime as base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY src/ src/
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run the app
CMD ["python", "src/app.py"]
