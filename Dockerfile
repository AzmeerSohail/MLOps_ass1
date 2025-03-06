# Use an official Python runtime as base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy application files (including model file)
COPY src/ src/
COPY requirements.txt .  # Copy dependencies file

# Ensure the model file is copied
COPY src/linear_regression_model.pkl src/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run the app
CMD ["python", "src/app.py"]
