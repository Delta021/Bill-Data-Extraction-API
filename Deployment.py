# Use official Python runtime as a parent image
FROM python: 3.10-slim

# Set working directory
WORKDIR / app

# Install system dependencies required for pdf2image (Poppler)
RUN apt-get update & & apt-get install - y \
    poppler-utils \
    & & rm - rf / var/lib/apt/lists/*

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install - -no-cache-dir - r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8000

# Run the application
CMD["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
