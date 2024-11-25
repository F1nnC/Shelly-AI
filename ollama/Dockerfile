# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /ollama

# Copy the current directory contents into the container at /ollama
COPY . /ollama

# Install Ollama
RUN pip install ollama

# Verify the installation of ollama and check if it includes an executable script
RUN pip show ollama

# Make port 11434 available to the world outside this container
EXPOSE 11434

# Run Ollama when the container launches, adjust the command if necessary
ENTRYPOINT ["ollama"]
CMD ["serve"]
