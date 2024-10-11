import os
import numpy as np
import shutil
import json
import csv
import os

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocess_utils import denormalize_img


def dict2str(model_params):
    if model_params is None:
        return " " 
    formatted_params = [f"{key}: {value}" for key, value in model_params.items()]
    return ', '.join(formatted_params)

def create_dir(dir_path):
    os.makedirs(dir_path, exist_ok=True)

def check_delete_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

# def write_csv(stats_dict, dir, file_name):
#     # Check if the file exists and has the correct column names
#     file_path = os.path.join(dir, file_name)
#     if not os.path.exists(file_path):
#         # Create the file and write the column names
#         create_dir(file_path)
#         with open(file_path, 'w', newline='') as csvfile:
#             fieldnames = [
#                 'Benchmark', 'Dataset', 'Preprocess', 'Model', 'Model_name', 
#                 'tp', 'fp', 'tn', 'fn', 'accuracy', 'precision', 'recall', 
#                 'specificity', 'mcc', 'auroc'
#             ]
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
    
#     # Append a new row to the CSV file
#     with open(file_path, 'a', newline='') as csvfile:
#         # fieldnames = [
#         #     'Benchmark', 'Dataset', 'Preprocess', 'Model', 'Model_name', 
#         #     'tp', 'fp', 'tn', 'fn', 'accuracy', 'precision', 'recall', 
#         #     'specificity', 'mcc', 'auroc'
#         # ]
#         # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writerow(stats_dict)

def write_json(dict, json_file_path):
    # Load existing logs if the file exists
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            old_data = json.load(f)
    else:
        old_data = []  # Initialize as an empty list if the file does not exist

    # Append new log data
    old_data.append(dict)  # Replace 'new_log_entry' with your actual log entry

    # Write updated logs back to the file
    with open(json_file_path, "w") as f:
        json.dump(old_data, f, indent=4)

    print("Updated log data")

def compute_stats(tn, tp, fp, fn):
    """
    Compute various measurement metrics from the given confusion matrix.

    Returns
        A dictionary containing the computed metrics.
    """
    # Compute the accuracy
    accuracy = (tp + tn) / (tp + tn + fp + fn)

    # Compute the precision
    precision = tp / (tp + fp) if tp + fp > 0 else 0

    # Compute the recall
    recall = tp / (tp + fn) if tp + fn > 0 else 0

    # Compute the specificity
    specificity = tn / (tn + fp) if tn + fp > 0 else 0

    # Compute the Matthews correlation coefficient (MCC)
    mcc_numerator = (tp * tn) - (fp * fn)
    mcc_denominator = ((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)) ** 0.5
    mcc = mcc_numerator / mcc_denominator if mcc_denominator != 0 else 0

    # Compute the AUROC (approximation)
    # Note: This is a simplified version and may not be as accurate as the library implementation
    auroc = 0.5 + ((tp - fn) * (tp + fn)) / (2 * (tp + fn) * (tn + fp))

    # Return the computed metrics
    stats_dir= {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "mcc": mcc,
        "auroc": auroc
    }

    return {key: round(value, 3) for key, value in stats_dir.items()}
