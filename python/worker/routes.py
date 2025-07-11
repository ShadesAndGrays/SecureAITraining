from flask import Blueprint, request, render_template, jsonify
from flask_cors import cross_origin
import pinata.routes as pin
from flasker.models.model import BaseModel
from flasker.models.classification import simulate as spam_simulate

import requests
import multiprocessing
import os

worker_bp=Blueprint('worker',__name__,url_prefix='/worker')

address_map = {"0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC":1,
"0x90F79bf6EB2c4f870365E785982E1f101E93b906":2,
"0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65":3,
"0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc":4,
"0x976EA74026E726554dB657fA54763abd0C3a0aa9":5,
"0x14dC79964da2C08b23698B3D3cc7Ca32193d9955":6,
"0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f":7,
"0xa0Ee7A142d267C1f36714E4a8F75612F20a79720":8
}

manager = multiprocessing.Manager()
worker_lock = multiprocessing.Lock()
worker_results = manager.dict()
worker_metrics = manager.dict()

worker_status = manager.Value('u','idle') # idle, working, done, failed


@worker_bp.route('/start-work', methods=['POST'])
@cross_origin(origin='*')
def start_work():
    with worker_lock:
        if worker_status.value in ['working','done','failed']:
            return jsonify({'message': f'Workers  are:  {worker_status.value}. Please wait or check status.'}), 409

    data = request.json
    print("\n\nworker: ",data)
    count = int(data.get('count'))
    cid = data.get('cid') 
    fl_type = data.get('flType')
    round_id = int(data.get('round'))
    participants = data.get('participants').split(',')

    # start(count,cid,fl_type,round_id,participants)
    new_process = multiprocessing.Process(target=_start_work,args=(count,cid,fl_type,round_id,participants,worker_status,worker_results,worker_lock,worker_metrics))
    new_process.start()

    global current_worker_process
    current_worker_process = new_process

    with worker_lock:
        worker_status.set('working')
        print(f"Flask Process: Started Working, status set to:{worker_status.value} ")
    return jsonify({'message': worker_status.value})


@worker_bp.route('/check-work', methods=['GET'])
@cross_origin(origin='*')
def check_workers_status():
    with worker_lock:
        print('Worker Statue: ',worker_status.value)
        return jsonify({'message':worker_status.value})
    return jsonify({'message': 'An error occured when getting aggregate status'}), 500

@worker_bp.route('/get-cids', methods=['GET'])
@cross_origin(origin='*')
def get_cids():
    global current_worker_process
    with worker_lock:
        if worker_status.value == 'done':
            current_worker_process.join()
            worker_status.set('idle')
            return jsonify(dict(worker_results))
        elif worker_status.value == 'failed':
            worker_status.set('idle')
            return jsonify({'message': 'Workers failed.', 'error_details': dict(worker_results.get('error', 'No details'))}), 500
            

    return jsonify(metrics.values)

@worker_bp.route('/get_metrics', methods=['GET'])
@cross_origin(origin='*')
def get_mertics():
    global worker_metrics
    return jsonify(dict(worker_metrics))

# @worker_bp.route('/start', methods=['POST'])
# @cross_origin(origin='*')
def _start_work(count,cid,fl_type,round_id,participants,shared_status,shared_result,shared_lock,shared_metrics):
    print ("starting work")
    with shared_lock:
        shared_status.set('working')

    models = []
    global metrics
    metrics = {}
    print("Selected Participants",participants)

    model_parameters_path = f'download/temp/aggregate_{fl_type}.joblib' # Example path
    pin.download(cid,model_parameters_path)
    match fl_type:
        case 'spam_classification':
            models,model_metrics = spam_simulate(count,model_parameters_path,round_id,participants)
            metrics = model_metrics 
        case _:
            return jsonify({"message":f" '{fl_type}' NOT IMPLEMEMTED"}), 500

    cids = []
    print(f"uploding {models}")
    for m in models:
        cid = pin.pinata_upload(m)
        cids.append(cid)
        print(f"uploaded {m}\ncid: {cid}\n\n\n")
    print("returning:",{'message' :'success', 'cids': cids, 'metrics': metrics } )

    with shared_lock:
        print('done working')
        shared_status.set('done')

        shared_result['cids'] = cids
        shared_result['metrics'] = metrics
        shared_metrics.update(metrics)

    return jsonify({'message' :'success', 'cids': cids, 'metrics': metrics })
