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

    model_parameters_path = f'download/temp/aggregate_{fl_type}.joblib' # Example path
    pin.download(cid,model_parameters_path)
    dataset_path = ""
    match fl_type:
        case 'spam_classification':
            models = spam_simulate(count,model_parameters_path,dataset_path,round_id)
        case _:
            return jsonify({"message":f" '{fl_type}' NOT IMPLEMEMTED"}), 500

    # model.set_parameters(param)
    # model.train_model(dataset_path,count)
    # print(model.evaluate_model(dataset_path,count))
    # model.save_model(local_model_filename)
    cids = []
    print(f"uploding {models}")
    for m in models:
        cid = pin.pinata_upload(m)
        cids.append(cid)
        print(f"uploaded {m}\ncid: {cid}\n\n\n")

    return jsonify({'message' :'success', 'cids': cids })

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