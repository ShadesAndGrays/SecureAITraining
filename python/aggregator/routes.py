from flask import Blueprint, request, render_template, jsonify
from flask_cors import cross_origin
import numpy as np
import pinata.routes as pin
from flasker.models.classification import SpamClassificationHandler
import os

aggregator_bp=Blueprint('aggregator',__name__,url_prefix='/aggregator')


     
@aggregator_bp.route('/aggregate', methods=['POST'])
@cross_origin(origin='*')
# take in cids and return an aggrgated cid 
def aggregate():
    data = request.json
    global_cid =  {}
    model_type = {}
    fl_type = data.get('flType')
    cids = data.get('cids')

    match fl_type:
        case "spam_classification":
            model_type = SpamClassificationHandler
            models:list[SpamClassificationHandler] = []
            for cid in cids:
                file = pin.pinata_download(cid,f'download/temp/aggregation_{cid}.joblib')
                models.append(model_type(model_path=file))
            global_model, acc, f1 = aggregate_spam_classificatoin(models)
            global_cid = pin.upload(global_model)
            return jsonify({
                'cid':global_cid,
                'accuracy': acc,
                'f1':f1
            })
    return global_cid

def aggregate_spam_classificatoin(parameters):
        global_model = SpamClassificationHandler()
        global_model._load_dataset(chuch_parts=40)
        cc, fc  = global_model.aggregate_mnb_models(parameters)
        global_model.set_parameters({'class_count_':cc,'feature_count_':fc})
        metrics = global_model.evaluate_model()
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