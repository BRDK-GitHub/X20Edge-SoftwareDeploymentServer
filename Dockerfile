# Use an official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port Quart runs on (adjust if needed)
EXPOSE 5000

# Run the Quart app - corresponds to quart run --host=0.0.0.0 --port=5000
CMD ["quart", "run", "--host=0.0.0.0", "--port=5000"]