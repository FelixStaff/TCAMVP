"""
This is a boilerplate pipeline 'deployment'
generated using Kedro 0.19.13
"""

import os
import pickle
import json
import numpy as np
from azureml.core.model import Model
from azureml.core import Run

# Load relevant fucntions from Azure ML 
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice

def init():
    global model
    # Azure ML mounts the model in a specific directory
    model_path = Model.get_model_path('CD_GH_Trained_Neural_Network')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

def run(raw_data):
    try:
        input_json = json.loads(raw_data)
        data = input_json['data']
        # If dicts, convert to list of lists
        if isinstance(data[0], dict):
            feature_order = input_json.get('feature_order')
            if not feature_order:
                return json.dumps({'error': 'feature_order must be provided if using dict input'})
            X = np.array([[row[feat] for feat in feature_order] for row in data])
        else:
            X = np.array(data)
        preds = model.predict(X)
        return json.dumps({'predictions': preds.tolist()})
    except Exception as e:
        return json.dumps({'error': str(e)})
