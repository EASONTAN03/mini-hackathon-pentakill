import os
import pandas as pd
import pdfplumber
# from docx import Document as DocxDocument
# from spire.doc import Document as SpireDocument
import re

# Text cleaning function
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    return clean_text(text)

# def extract_text_from_docx(file_path):
#     doc = DocxDocument(file_path)
#     text = ' '.join(paragraph.text for paragraph in doc.paragraphs)
#     return clean_text(text)

# def extract_text_from_doc(file_path):
#     doc = SpireDocument()
#     doc.LoadFromFile(file_path)
#     text = doc.GetText()
#     return clean_text(text)

def process_files(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        # elif filename.endswith('.docx'):
        #     text = extract_text_from_docx(file_path)
        # elif filename.endswith('.doc'):
        #     text = extract_text_from_doc(file_path)
        else:
            continue  # Skip non-supported file types
        data.append({'name': filename, 'ocr': text})
    return pd.DataFrame(data)

def save_csv(input_dir):
    # Set the folder path using the current working directory
    current_directory = os.getcwd()  # Get the current working directory
    folder_name = 'output'
    folder_path = os.path.join(current_directory, folder_name)  # Combine paths
    os.makedirs(folder_path, exist_ok=True)

    # Process files and create a DataFrame
    df = process_files(input_dir)

    # Specify the output path for the CSV file in the current directory
    output_csv_path = os.path.join(current_directory, 'output', 'resumes.csv')

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv_path, index=False)

    return output_csv_path

def delete_all_files_in_directory(directory_path):
    # Ensure the provided path is a directory
    if not os.path.isdir(directory_path):
        print(f"The path {directory_path} is not a valid directory.")
        return

    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            os.remove(file_path)  # Delete the file
            print(f"Deleted file: {file_path}")
        else:
            print(f"Skipped directory: {file_path}")