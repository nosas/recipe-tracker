# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app

# Copy the relevant directories and files into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8050

# Run app.py when the container launches
CMD ["python", "./tracker/app.py"]
