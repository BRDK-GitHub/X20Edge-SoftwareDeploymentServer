from quart import Quart, render_template, jsonify, request, redirect, url_for, send_from_directory
import zipfile
from werkzeug.utils import secure_filename
import shutil
from readLogger import readVersion
from browseBuRPLC import scan_subnet
import os

app = Quart(__name__)

UPLOAD_FOLDER = 'zip_data'
FTP_FOLDER = 'ftp_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FTP_FOLDER'] = FTP_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB limit
# If folders doesn't exist create it
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FTP_FOLDER, exist_ok=True)

@app.route("/")
async def index():
    return await render_template("index.html")

@app.route('/getVersion', methods=['GET'])
async def getVersion():
    ip = request.args.get('ip')
    result = await readVersion(ip)
    return jsonify(result)

#Example: localhost:5000/browse?subnet=192.168.30.0
@app.route('/browse', methods=['GET'])
async def browse():
    subnet = request.args.get('subnet')
    if not subnet:
        return jsonify({"error": "No subnet provided"}), 400

    subnet = subnet+"/24"
    port = 11169                         # Scan ANSL port to find B&R PLCs
    BuR_ips = scan_subnet(subnet, port) 

    return jsonify({"BuR_ips": BuR_ips})

@app.route('/listFolders', methods=['GET'])
async def listFolders():
    folder_path = app.config['FTP_FOLDER']
    print(folder_path)
    try:
        folders = []
        for folder in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, folder)):
                folders.append(folder)

        return jsonify(folders)
    except Exception as e:
        return {"error": str(e)}, 500


# FILE UPLOAD:

@app.route('/upload', methods=['POST'])
async def upload_file():
    files = await request.files  # Await the async property
    if 'zipFile' not in files:
        return "No file part", 400

    file = files['zipFile']
    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.zip'):
        filename = secure_filename(file.filename)
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the .zip file to UPLOAD_FOLDER
        await file.save(zip_path)

        # Extract the .zip file to FTP_FOLDER
        extract_folder = os.path.join(app.config['FTP_FOLDER'], os.path.splitext(filename)[0])
        os.makedirs(extract_folder, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

        # Optionally delete the .zip file from UPLOAD_FOLDER after extraction
        os.remove(zip_path)

        return await render_template('index.html')
        #return f"File extracted to {extract_folder}"

    return "Invalid file type. Only .zip files are allowed.", 400

@app.route('/deleteFolder', methods=['POST'])
async def deleteFolder():
    data = await request.get_json()
    folder_name = data.get('folderName')

    if not folder_name:
        return "Folder name is required.", 400

    folder_path = os.path.join(app.config['FTP_FOLDER'], folder_name)

    try:
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)  # Recursively delete the folder
            return {"message": f"Folder '{folder_name}' deleted successfully."}, 200
        else:
            return f"Folder '{folder_name}' does not exist.", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.errorhandler(413)
async def request_entity_too_large(error):
    return "File is too large. Maximum size is 100 MB.", 413


if __name__ == "__main__":
    # when calling directly from python use development mode (production will use "quart run")
    os.environ['QUART_ENV'] = 'development'
    os.environ['QUART_DEBUG'] = '1'
    app.run(host='0.0.0.0', port=5000)