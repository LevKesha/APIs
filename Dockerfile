# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy the requirements file if you have one, else install directly
# For this example, we'll install Flask, Flask-RESTful, and boto3 directly
RUN pip install --upgrade pip && \
    pip install flask flask-restful boto3

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
