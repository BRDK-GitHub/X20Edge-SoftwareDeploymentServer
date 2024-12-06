from quart import Quart, render_template, jsonify, request
from readLogger import readVersion
from browseBuRPLC import scan_subnet
import os

app = Quart(__name__)

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



if __name__ == "__main__":
    # when calling directly from python use development mode (production will use "quart run")
    os.environ['QUART_ENV'] = 'development'
    os.environ['QUART_DEBUG'] = '1'
    app.run(host='0.0.0.0', port=5000)