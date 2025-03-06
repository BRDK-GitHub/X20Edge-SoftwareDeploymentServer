from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the authorizer
authorizer = DummyAuthorizer()

# Get FTP credentials and home directory
ftp_user_name = os.getenv("FTP_USER_NAME")
ftp_user_pass = os.getenv("FTP_USER_PASS")
ftp_user_home = os.getenv("FTP_USER_HOME", "./ftp_data")  # Default directory

# Add user
authorizer.add_user(ftp_user_name, ftp_user_pass, ftp_user_home, perm="elradfmw")

# Set up FTP handler
handler = FTPHandler
handler.authorizer = authorizer


# Enable Passive Mode
handler.passive_ports = range(30000, 30010)
handler.masquerade_address = os.getenv("FTP_HOST_IP")

# Set up and start the FTP server
server = FTPServer(("0.0.0.0", 21), handler)

print("FTP server is running...")
server.serve_forever()
