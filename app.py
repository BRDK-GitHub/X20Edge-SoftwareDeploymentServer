from flask import Flask, render_template, jsonify, request
from readLogger import readVersion
import os
import asyncio

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route('/getVersion', methods=['GET']) 
def getVersion():
	ip = request.args.get('ip')
	loop = asyncio.new_event_loop() 
	asyncio.set_event_loop(loop) 
	result = loop.run_until_complete(readVersion(ip)) 
	return result


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)