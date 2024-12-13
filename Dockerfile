# Use official Python image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from current directory to working directory in container
# Note: Change the copy path to ensure we copy the app directory correctly
COPY ./app ./app
COPY ./app/main.py .

# Expose port 8000
EXPOSE 8000

# Command to run the application
# Note: Changed the command to correctly reference the app module
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]