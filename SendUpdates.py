import ftplib
import os
import json
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_file(ftp, file_path, remote_path):
    """Upload a file to the FTP server, overwriting if it exists."""
    with open(file_path, 'rb') as file:  # Open in binary mode
        ftp.storbinary(f'STOR {remote_path}', file)

def upload_folder(ftp, folder_path, remote_folder_path):
    """Upload a folder and its contents to the FTP server, creating directories as needed."""
    for root, dirs, files in os.walk(folder_path):
        for dirname in dirs:
            local_dir_path = os.path.join(root, dirname)
            remote_dir_path = os.path.join(remote_folder_path, os.path.relpath(local_dir_path, start=folder_path))
            try:
                ftp.mkd(remote_dir_path)
                #print(f"Created directory {remote_dir_path}")
            except ftplib.error_perm as e:
                # Ignore "directory already exists" error
                if not str(e).startswith('550'):
                    raise
                #print(f"Directory {remote_dir_path} already exists")

        for filename in files:
            local_file_path = os.path.join(root, filename)
            remote_file_path = os.path.join(remote_folder_path, os.path.relpath(local_file_path, start=folder_path))
            with open(local_file_path, 'rb') as file:  # Open in binary mode
                ftp.storbinary(f'STOR {remote_file_path}', file)
                #print(f"Uploaded file {remote_file_path}")

# Recursive function to delete directory
def delete_ftp_directory(ftp, path):
    # List all files and directories in the current path

    items = ftp.nlst(path)
    
    for item in items:
        # Construct the full path
        full_path = f"{path}/{item}"
        
        try:
            # Try to change to directory (to check if it's a directory)
            ftp.cwd(full_path)
            # If successful, recursively delete its contents
            delete_ftp_directory(ftp, full_path)
            # Delete the directory after its contents have been deleted
            ftp.rmd(full_path)
            #print(f"Deleted directory: {full_path}")
        except ftplib.error_perm as e:
            # If it's not a directory, delete the file
            if str(e).startswith('550'):
                ftp.delete(full_path)
                #print(f"Deleted file: {full_path}")
            else:
                logging.error(f"Error deleting file or folder with error: {e}")


def upload_to_ftp_server(server, username, password, folder_path, remote_folder_path, file_path):
    """Upload the specified folder and file to a single FTP server."""
    try:
        ftp = ftplib.FTP(server)
        ftp.login(username, password)
        #print(f"Connected to {server}")
        logging.info(f"Connected to {server}")

        # Change to the root directory
        ftp.cwd('/')

        # Upload folder "Default_X20CP04xx"
        folder_name = os.path.basename(folder_path)
        try:
            ftp.mkd(folder_name)
            #print(f"Created root directory {folder_name}")
        except ftplib.error_perm as e:
            if not str(e).startswith('550'):
                raise
            #print(f"Root directory {folder_name} already exists")

        upload_folder(ftp, folder_path, folder_name)
        
        # Upload file "arnbcfg.xml" to the root directory
        remote_file_path = os.path.basename(file_path)
        upload_file(ftp, file_path, remote_file_path)

        # Upload folder "Default_X20CP04xx_RemoteInstall" or delete if it doesn't exist
        remote_folder_name = os.path.basename(remote_folder_path)
        if os.path.exists(remote_folder_path) and os.path.isdir(remote_folder_path):
            # If folder exists send it to the FTP server
            try:
                ftp.mkd(remote_folder_name)
            except ftplib.error_perm as e:
                if not str(e).startswith('550'):
                    raise
            upload_folder(ftp, remote_folder_path, remote_folder_name)
        else:
            # Folder doesn't exist, check if the ftp server has the folder and delete it if it exists.
            try:
                ftp.cwd(remote_folder_name)
                # If no exception is raised, the folder exists and we should delete it.
                ftp.cwd('/')
                root_directory = f"/{remote_folder_name}"
                delete_ftp_directory(ftp, root_directory)
                ftp.cwd('/')
                ftp.rmd(remote_folder_name)
            except ftplib.error_perm as e:
                if not str(e).startswith('550'): # 550 means 'No such file or directory'
                    # If the error is not 550, raise it
                    raise

        ftp.quit()
    
        logging.info(f"Uploaded folder and file to {server}")
    except ftplib.all_errors as e:
        logging.error(f" Failed to upload to {server} with error: {e}")

def upload_to_ftp_servers(servers, username, password, folder_path, remote_folder_path, file_path):
    """Upload the specified folder and file to a list of FTP servers."""
    with ThreadPoolExecutor(max_workers=36) as executor:
        futures = [
            executor.submit(upload_to_ftp_server, server, username, password, folder_path, remote_folder_path, file_path)
            for server in servers
        ]
        for future in futures:
            future.result()  # Wait for all futures to complete


