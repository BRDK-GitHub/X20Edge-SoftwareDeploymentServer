FROM python:3.11-slim

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install pyftpdlib python-dotenv

# Expose passive mode ports
EXPOSE 21 30000-30010


CMD ["python", "FtpServer.py"]