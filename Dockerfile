# Use an official Python runtime as a parent image
FROM python:3.12.0-alpine

# Set environment variables for Flask and Gunicorn
ENV APP_MODULE=main:app
ENV HOST=0.0.0.0
ENV PORT=8000

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that your FastAPI application will run on
EXPOSE $PORT
# Define the command to run your FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
