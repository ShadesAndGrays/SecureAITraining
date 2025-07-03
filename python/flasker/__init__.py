from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os
import sqlite3

app = Flask(__name__, instance_relative_config=True)
CORS(app, support_credentials=True)
DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # use column names
    return conn

@app.route('/propose', methods=['POST'])
@cross_origin(origin='*')
def propose():
    return jsonify({"message":"Success"})

@app.route('/heartbeat', methods=['GET'])
@cross_origin(origin='*')
def check_health():
    return "To the beat of the drum"

if __name__ == '__main__':
    app.run(debug=True)