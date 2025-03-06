# Use Python 3.9 (or later)
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY src/ src/
COPY frontend/ frontend/  
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 5000

# Command to run the app
CMD ["python", "src/app.py"]
