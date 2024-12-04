from quart import Quart, render_template, jsonify, request
from readLogger import readVersion
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

if __name__ == "__main__":
    app.run()