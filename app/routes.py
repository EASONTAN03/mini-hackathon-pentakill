from flask import Blueprint, render_template, request, jsonify
from app import app 
import os 
from .utils.gpt_openai import *
from .utils.files2csv import *

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('ThirdFrontEnd.html')

@bp.route('/upload', methods=['POST'])
def upload_files():
    # Get the absolute path of the folder where this script is running
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Define separate directories for CVs and JDs
    Upload_CV = os.path.join(current_directory, 'upload_cv')
    Upload_JD = os.path.join(current_directory, 'upload_jd')

    # Ensure both 'upload_CV' and 'upload_JD' folders exist
    if not os.path.exists(Upload_CV):
        os.makedirs(Upload_CV)

    if not os.path.exists(Upload_JD):
        os.makedirs(Upload_JD)
    # Check if the request contains files for both CV and JD
    if 'cv_files' not in request.files and 'jd_files' not in request.files:
        print("No files were uploaded.")
        return jsonify({'message': 'No files part'}), 400

    # Initialize counters for uploaded files
    saved_cv_files = 0
    saved_jd_files = 0

    # Handling CV Files
    if 'cv_files' in request.files:
        cv_files = request.files.getlist('cv_files')
        print(f"Number of CV files to upload: {len(cv_files)}")
        for file in cv_files:
            if file and file.filename != '':
                file_path = os.path.join(Upload_CV, file.filename)
                try:
                    file.save(file_path)
                    saved_cv_files += 1
                    print(f"CV file saved: {file_path}")
                except Exception as e:
                    print(f"Failed to save CV file: {file.filename}, Error: {str(e)}")
                    return jsonify({'message': f'Error saving CV file: {file.filename}', 'error': str(e)}), 500
            else:
                print("Empty CV file encountered.")

    # Handling JD Files
    if 'jd_files' in request.files:
        jd_files = request.files.getlist('jd_files')
        print(f"Number of JD files to upload: {len(jd_files)}")
        for file in jd_files:
            if file and file.filename != '':
                file_path = os.path.join(Upload_JD, file.filename)
                try:
                    file.save(file_path)
                    saved_jd_files += 1
                    print(f"JD file saved: {file_path}")
                except Exception as e:
                    print(f"Failed to save JD file: {file.filename}, Error: {str(e)}")
                    return jsonify({'message': f'Error saving JD file: {file.filename}', 'error': str(e)}), 500
            else:
                print("Empty JD file encountered.")

    return jsonify({
        'message': 'Files uploaded successfully',
        'cv_files_saved': saved_cv_files,
        'jd_files_saved': saved_jd_files
    }), 200


@bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message')
    # Process files if any
    resume_path = save_csv("upload_cv","resume.csv")
    jd_path= save_csv("upload_jd","jd.csv")
    print("Done extract csv")

    df,jd_df=process_files(resume_path,jd_path)
    print("Done processed resume")

    prompts = generate_prompts(df, jd_df["ocr"][0], user_input)
    ai_response = get_ai_response(prompts,"AZURE_OPENAI_GPT4_ENDPOINT")
    print("Done ai reponse")


    delete_all_files_in_directory("upload_cv")

    if isinstance(ai_response, str):
        return jsonify({'ai_response': ai_response})
    else:
        return jsonify({'error': 'Unexpected error occurred'}), 500