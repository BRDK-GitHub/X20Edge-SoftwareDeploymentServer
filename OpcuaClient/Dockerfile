# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the script and requirements
COPY . .

# Install the required dependencies
RUN pip install asyncua

# Run the OPC UA client script
CMD ["python", "opcuaclient.py"]
