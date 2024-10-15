from flask import Blueprint, render_template, request, jsonify
from app import app 
import os 
from .utils.textract import process_pdfs_and_save_combined
from .utils.openai import get_ai_response

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('ThirdFrontEnd.html')

@bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message')
    files = request.files.getlist('files')
    file_names = []

    for file in files:
        if file:  # Check if file is not empty
            # Save the file to the specified upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            file_names.append(file.filename)  # Store the file name for response


    # Process files if any
    candidate_text = ""
    if files:
        candidate_text = process_pdfs_and_save_combined(files)

    # Combine user input with candidate text
    combined_text = f"{candidate_text}\n{user_input}"

    # Get AI response
    ai_response = get_ai_response(combined_text)

    if isinstance(ai_response, str):
        return jsonify({'ai_response': ai_response})
    else:
        return jsonify({'error': 'Unexpected error occurred'}), 500