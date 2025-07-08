from flask import Blueprint, request, render_template, jsonify
from flask_cors import cross_origin
import numpy as np
import pinata.routes as pin
from flasker.models.classification import SpamClassificationHandler
import os
import multiprocessing
import time

aggregator_bp=Blueprint('aggregator',__name__,url_prefix='/aggregator')


manager = multiprocessing.Manager()
aggregate_lock = multiprocessing.Lock()
aggregated_result = manager.dict()
aggregate_process = manager.dict()

aggregate_status = manager.Value('u','idle') # idle, working, done, failed

@aggregator_bp.route('/start-aggregate', methods=['POST'])
@cross_origin(origin='*')
def start_aggregation():
    with aggregate_lock:
        if aggregate_status.value in ['working', 'done', 'failed']:
            return jsonify({'message': f'Aggregation is already {aggregate_status.value}. Please wait or check status.'}), 409

    data = request.json
    fl_type = data.get('flType')
    cids = data.get('cids').split(',')
    round_id = data.get('round')
    new_process = multiprocessing.Process(target=_start_aggregate,args=(fl_type,cids,round_id,aggregate_status,aggregated_result,aggregate_lock))
    new_process.start()

    global current_aggregate_process
    current_aggregate_process = new_process

    with aggregate_lock:
            aggregate_status.set('working') # Set to working immediately after starting the process
            print(f"Flask process: Started aggregation, status set to: {aggregate_status.value}")

    return jsonify({'message': aggregate_status.value})


@aggregator_bp.route('/check-aggregate', methods=['GET'])
@cross_origin(origin='*')
def check_aggregate_status():
    global aggregate_status
    with aggregate_lock:
        print('aggregate status: ',aggregate_status.value)
        return jsonify({'message':aggregate_status.value})
    return jsonify({'message': 'An error occured when getting aggregate status'}), 500

@aggregator_bp.route('/get-aggregated-cid', methods=['GET'])
@cross_origin(origin='*')
def get_result():
    global current_aggregate_process
    with aggregate_lock:
        if aggregate_status.value == 'done':
            current_aggregate_process.join()
            aggregate_status.set('idle') 
            return jsonify(dict(aggregated_result))

        elif aggregate_status.value == 'failed':
            aggregate_status.set('idle') 
            return jsonify({'message': 'Aggregation failed.', 'error_details': dict(aggregated_result.get('error', 'No details'))}), 500
        else: # idle or other states
            return jsonify({'message': 'No aggregation has completed yet or is running.'}), 404
    pass

# sub process
# take in cids and return an aggrgated cid 
# Love hate relationship IPC
def _start_aggregate(fl_type,cids,round_id,shared_status,shared_result,shared_lock):
    # data = request.json
    print("strarting work")
    with shared_lock:
        shared_status.set('working') 

    match fl_type:
        case "spam_classification":
            models:list[SpamClassificationHandler] = []
            for cid in cids:
                file = pin.pinata_download(cid,f'download/temp/aggregation_{cid}.joblib')
                models.append(SpamClassificationHandler(model_path=file).extract_parameters())
            global_model, acc, f1 = aggregate_spam_classificatoin(models)
            global_cid = pin.pinata_upload(global_model.save_parameters(f'download/temp/global_aggregation_classification_{round_id}.joblib'))
            with shared_lock:
                print('done training')
                shared_status.set('done')
                shared_result['cid'] = global_cid
                shared_result['accuracy'] = acc
                shared_result['f1'] = f1

def aggregate_spam_classificatoin(parameters):
        global_model = SpamClassificationHandler(initial=True)
        cc, fc  = global_model.aggregate_mnb_models(parameters)
        global_model.set_parameters({'class_count_':cc,'feature_count_':fc})
        global_model._load_dataset()
        metrics = global_model.evaluate_model(test_fraction=0.008)
        return global_model, metrics['accuracy'], metrics['f1'] 



"""
weights_list: List of model weights. Each element is a list of numpy arrays (one per layer).
"""
    # FedAvg
def aggregate(weights_list):
    """
    Returns the element-wise average of the weights across all models.
    """
    # Transpose the list to group weights by layer
    # Each element in 'layer_weights' is a list of arrays for that layer from all models
    layer_weights = list(zip(weights_list))
    # Average each layer's weights
    aggregated = [np.mean(np.stack(w), axis=0) for w in layer_weights]
    return aggregated