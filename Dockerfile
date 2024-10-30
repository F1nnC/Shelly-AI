# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expose the correct port for the Flask app
EXPOSE 8012

# Run the Flask application on the correct port
CMD ["flask", "run", "--host=0.0.0.0", "--port=8012"]
