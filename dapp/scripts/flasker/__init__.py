from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os

def create_app(test_config = None):
    # Create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, support_credentials=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
         os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/calculate', methods=['GET'])
    @cross_origin(origin='*')
    def calculate():
    # Example function: Calculate factorial
        number = request.args.get('number', default=1, type=int)
        result = factorial(number)
        return jsonify({'result': result})
    
    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * factorial(n-1)
    
    return app