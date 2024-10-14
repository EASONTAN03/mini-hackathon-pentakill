import yaml
import os 
import numpy as np
import pandas as pd
import json
# import shutil  # Import shutil to copy files
import random

# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
# import operation_utils as utils
# import preprocess_utils as preprocess
# current_dir = os.getcwd()

# with open('config.yaml', 'r') as file:
#     config = yaml.safe_load(file)

# interim_data_path = config['dataset']['interim']
# processed_data_path = config['dataset']['processed']
# dataset = config['configs']['dataset']
# benchmark = config['configs']['benchmark']

# with open('params.yaml', 'r') as file:
#     params = yaml.safe_load(file)
# seed = params['make_dataset']['seed']

# param_prepare = params['prepare']
# prepare_benchmark = param_prepare['benchmark']
# train_test = param_prepare['train_test']
# resize = tuple(param_prepare['resize'])
# color = param_prepare['color_mode']
# normalize = param_prepare['normalize']
# param_filter=param_prepare['filter']
# filter = param_filter['method']
# param_feature=param_prepare['feature_extract']
# feature_extract = param_feature['method']

# np.random.seed(seed)
# random.seed(seed)

# # Define input and output directories
# data_dir = f'{dataset}_{benchmark}'
# input_dir = os.path.join(interim_data_path, data_dir)
# output_dir = os.path.join(processed_data_path, data_dir, train_test)
# images_dir = os.path.join(input_dir, train_test)

from azure.storage.blob import BlobServiceClient

# Replace with your Blob Storage account URL and credentials
storage_account_url = "https://resumedatastorage.blob.core.windows.net"
container_name = "input"
sas_token = "sp=racwdl&st=2024-10-14T07:13:39Z&se=2024-10-19T15:13:39Z&spr=https&sv=2022-11-02&sr=c&sig=mKk5vx48gOTYE30Z29zcVc3F0mZqDpyuFM6zuMahOqI%3D"

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url=storage_account_url, credential=sas_token)

# Get the container client
container_client = blob_service_client.get_container_client(container_name)

# List all the blobs (files) in the container
print("Listing blobs in the container:")
blob_list = container_client.list_blobs()

for blob in blob_list:
    print(blob.name)

"""
This code sample shows Custom Extraction Model operations with the Azure Form Recognizer client library. 
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""


from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""
endpoint = "YOUR_FORM_RECOGNIZER_ENDPOINT"
key = "YOUR_FORM_RECOGNIZER_KEY"

model_id = "YOUR_CUSTOM_BUILT_MODEL_ID"
formUrl = "YOUR_DOCUMENT"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Make sure your document's type is included in the list of document types the custom model can analyze
poller = document_analysis_client.begin_analyze_document_from_url(model_id, formUrl)
result = poller.result()

for idx, document in enumerate(result.documents):
    print("--------Analyzing document #{}--------".format(idx + 1))
    print("Document has type {}".format(document.doc_type))
    print("Document has confidence {}".format(document.confidence))
    print("Document was analyzed by model with ID {}".format(result.model_id))
    for name, field in document.fields.items():
        field_value = field.value if field.value else field.content
        print("......found field of type '{}' with value '{}' and with confidence {}".format(field.value_type, field_value, field.confidence))


# iterate over tables, lines, and selection marks on each page
for page in result.pages:
    print("\nLines found on page {}".format(page.page_number))
    for line in page.lines:
        print("...Line '{}'".format(line.content.encode('utf-8')))
    for word in page.words:
        print(
            "...Word '{}' has a confidence of {}".format(
                word.content.encode('utf-8'), word.confidence
            )
        )
    for selection_mark in page.selection_marks:
        print(
            "...Selection mark is '{}' and has a confidence of {}".format(
                selection_mark.state, selection_mark.confidence
            )
        )

for i, table in enumerate(result.tables):
    print("\nTable {} can be found on page:".format(i + 1))
    for region in table.bounding_regions:
        print("...{}".format(i + 1, region.page_number))
    for cell in table.cells:
        print(
            "...Cell[{}][{}] has content '{}'".format(
                cell.row_index, cell.column_index, cell.content.encode('utf-8')
            )
        )
print("-----------------------------------")





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