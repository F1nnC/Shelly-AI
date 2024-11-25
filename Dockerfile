# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /python

# Copy only the dependencies file first to leverage Docker cache
COPY requirements.txt .

# Install system dependencies and Python requirements
RUN apt-get update && apt-get install -y curl procps && \
    pip install --no-cache-dir -r requirements.txt

# Install Ollama, add it to PATH, and verify installation
RUN curl -fsSL https://ollama.com/install.sh | sh && \
    ln -s /usr/local/bin/ollama /usr/bin/ollama && \
    ollama --version

# Pull the required model and ensure it is accessible
RUN ollama serve & sleep 5 && ollama pull llama3.2:1b && pkill ollama

# Copy the rest of the application code
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=python/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expose both Flask and Ollama ports
EXPOSE 8012 11434

# Command to run both the Flask app and the Ollama service
CMD ["sh", "-c", "ollama serve & flask run --host=0.0.0.0 --port=8012"]
