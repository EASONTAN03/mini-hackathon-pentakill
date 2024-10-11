import yaml
import os 
import cv2
import numpy as np
import pandas as pd
import json
import shutil  # Import shutil to copy files
import random

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
import operation_utils as utils
import preprocess_utils as preprocess
current_dir = os.getcwd()

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

interim_data_path = config['dataset']['interim']
processed_data_path = config['dataset']['processed']
dataset = config['configs']['dataset']
benchmark = config['configs']['benchmark']

with open('params.yaml', 'r') as file:
    params = yaml.safe_load(file)
seed = params['make_dataset']['seed']

param_prepare = params['prepare']
prepare_benchmark = param_prepare['benchmark']
train_test = param_prepare['train_test']
resize = tuple(param_prepare['resize'])
color = param_prepare['color_mode']
normalize = param_prepare['normalize']
param_filter=param_prepare['filter']
filter = param_filter['method']
param_feature=param_prepare['feature_extract']
feature_extract = param_feature['method']

np.random.seed(seed)
random.seed(seed)

# Define input and output directories
data_dir = f'{dataset}_{benchmark}'
input_dir = os.path.join(interim_data_path, data_dir)
output_dir = os.path.join(processed_data_path, data_dir, train_test)
images_dir = os.path.join(input_dir, train_test)




# log_data = {
#     "dataset": data_dir,
#     "prepare_benchmark": prepare_benchmark,
#     "seed": seed,
#     "feature_extract_method": feature_extract_method,
#     "features_shape": extracted_features.shape,
#     "output_dir": output_dir
# }

# # Path to log file
# log_file_path = os.path.join(output_dir, "log.json")
# utils.write_json(log_data, log_file_path)