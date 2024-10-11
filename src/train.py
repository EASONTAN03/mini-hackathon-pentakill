import yaml
import csv
import os 
import cv2
import numpy as np
import pandas as pd
import json
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import random
import joblib

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
import operation_utils as utils
import modeling_utils as modeling
current_dir = os.getcwd()

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

processed_data_path = config['dataset']['processed']
output_model_path = config['output']['models']
dataset = config['configs']['dataset']
benchmark = config['configs']['benchmark']

with open('params.yaml', 'r') as file:
    params = yaml.safe_load(file)
seed = params['make_dataset']['seed']
prepare_benchmark = params['prepare']['benchmark']
param_train = params['train']
model_benchmark=param_train['model_benchmark']
model=param_train['model']
param_model = params['train'][f"{model}"]
split_ratio=param_train['split_ratio']
scale_features=param_train['scale_features']
train=param_train['train']


np.random.seed(seed)
random.seed(seed)

data_dir = f'{dataset}_{benchmark}'
processed_data_dir = f'{dataset}_{benchmark}_{prepare_benchmark}'
output_dir = os.path.join(output_model_path, processed_data_dir)
utils.create_dir(output_dir)
output_model_dir = os.path.join(output_dir, model)
utils.create_dir(output_model_dir)
model_path = f'{dataset}_{benchmark}_{prepare_benchmark}_{model_benchmark}'

input_dir = os.path.join(processed_data_path, data_dir, 'train')
features_path = os.path.join(input_dir,f'features_{prepare_benchmark}.npy')    

# joblib.dump(trained_model, model_path_dir)

try:
    trained_model = trained_model[0]
except Exception as e:
    print(e)


# log_data = {
#     "model_path": model_path,
#     "model_benchmark": model_benchmark,
#     "features_dir": processed_data_dir,
#     "seed": seed,
#     "features_shape": features.shape,
#     "output_dir": output_model_dir,
# }

# # Path to log file
# log_file_path = os.path.join(output_dir, "log.json")
# utils.write_json(log_data, log_file_path)

# # Write statistics to CSV
# header = ["model_path", "model", "tp", "fp", "tn", "fn", "accuracy", "precision", "recall", "specificity", "mcc", "auroc"]

# stats_file_path = os.path.join(output_model_path, "model_stats.csv")
# file_exists = os.path.isfile(stats_file_path)

# with open(stats_file_path, mode='a', newline='') as file:
#     writer = csv.writer(file)
#     # Write header if the file does not exist
#     if not file_exists:
#         writer.writerow(header)
#     # Write the statistics
#     writer.writerow([model_path, model_params, tp, fp, tn, fn, stats["accuracy"], stats["precision"], stats["recall"], 
#                      stats["specificity"], stats["mcc"], stats["auroc"]])