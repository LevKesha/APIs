# Use an updated Python slim image
FROM python:3.13-slim

# Set environment variables using the recommended "KEY=value" format
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Upgrade pip and install required packages
RUN pip install --upgrade pip && \
    pip install flask flask-restful boto3

# Copy the application code into the container
COPY . /app

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
