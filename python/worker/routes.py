from flask import Blueprint, request, render_template, jsonify
from flask_cors import cross_origin
import pinata.routes as pin
from flasker.models.model import BaseModel
from flasker.models.classification import simulate as spam_simulate

import requests
import threading
import os

worker_bp=Blueprint('worker',__name__,url_prefix='/worker')

@worker_bp.route('/start', methods=['POST'])
@cross_origin(origin='*')
def start():
    models = []
    data = request.json
    print("\n\nworker: ",data)
    count = int(data.get('count'))
    cid = data.get('cid') 
    fl_type = data.get('flType')
    round_id = int(data.get('round'))

    local_model_filename = f'download/temp/{fl_type}.joblib' # Example path
    dataset_path = ""
    match fl_type:
        case 'spam_classification':
            dataset_path = "data/classification_dataset/spam_data.csv"
            models = spam_simulate(count,local_model_filename,dataset_path,round_id)
        case _:
            return jsonify({"message":f" '{fl_type}' NOT IMPLEMEMTED"}), 500

    # model.set_parameters(param)
    # model.train_model(dataset_path,count)
    # print(model.evaluate_model(dataset_path,count))
    # model.save_model(local_model_filename)
    for m in models:
        cid = pin.pinata_upload(m)
        print(f"upload {m}\ncid: {cid}\n\n\n")

    return jsonify({'message' :'success'})

# @worker.route('/propose', methods=['POST'])
# @cross_origin(origin='*')
# def propose():
#     # create model
#     data = request.json
#     fl_type = data.get('flType')
#     model:BaseModel = {}
#     match fl_type:
#         case 'spam_classification':
#             model = SpamClassificationHandler()
#         case _:
#             return jsonify({"message":f" '{fl_type}' NOT IMPLEMEMTED"}), 500
#     # Extrart parameters
#     file_path = 'download/temp/model.joblib'
#     model.save_model(file_path)
#     # Upload parameters
#     cid = pin.pinata_upload(file_path)
#     # return cid
#     return jsonify({"message":"Success","cid":cid})