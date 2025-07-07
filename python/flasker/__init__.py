from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os
import sqlite3
import pinata.routes as pin
from pinata.routes import pinata_bp
from worker.routes import worker_bp
from aggregator.routes import aggregator_bp
from flasker.models.model import BaseModel
from flasker.models.classification import SpamClassificationHandler

if os.getenv('FLASK_ENV') == 'development':
    from dotenv import load_dotenv
    load_dotenv() # Load .env file only if in development
    print("Running in Development")
elif os.getenv('FLASK_ENV') == 'production':
    print("Running in production")
    pass

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(pinata_bp)
app.register_blueprint(worker_bp)
app.register_blueprint(aggregator_bp)
CORS(app, support_credentials=True)
DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # use column names
    return conn

@app.route('/propose', methods=['POST'])
@cross_origin(origin='*')
def propose():
    # create model
    data = request.json
    fl_type = data.get('flType')
    model:BaseModel = {}
    match fl_type:
        case 'spam_classification':
            model = SpamClassificationHandler()
        case _:
            return jsonify({"message":f" '{fl_type}' NOT IMPLEMEMTED"}), 500
    # Extrart parameters
    file_path = f'download/temp/{fl_type}.joblib'
    model.save_model(file_path)
    # Upload parameters
    cid = pin.pinata_upload(file_path)
    # return cid
    return jsonify({"message":"Success","cid":cid})

@app.route('/heartbeat', methods=['GET'])
@cross_origin(origin='*')
def check_health():
    return "To the beat of the drum"

if __name__ == '__main__':
    app.run(debug=True)