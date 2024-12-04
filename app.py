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

#Example: localhost:5000/browse?subnet=192.168.30.0/24
@app.route('/browse', methods=['GET'])
async def browse():
    subnet = request.args.get('subnet')
    if not subnet:
        return jsonify({"error": "No subnet provided"}), 400

    port = request.args.get('port', default=11169, type=int)
    open_ips = scan_subnet(subnet, port)

    return jsonify({"open_ips": open_ips})



if __name__ == "__main__":
    app.run()