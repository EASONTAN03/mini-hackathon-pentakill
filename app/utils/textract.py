import docx
import re
import glob
from PyPDF2 import PdfReader

def docx_to_text(word_file):
    doc = docx.Document(word_file)
    full_text = []

    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)

    text = ' '.join(full_text).lower().strip()
    text = re.sub('\s+', ' ', text)  # Normalize spaces
    return text

# Function to convert a single PDF to cleaned text
def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page_num in range(len(reader.pages)):
        page_text = reader.pages[page_num].extract_text()
        if page_text:
            cleaned_text = ' '.join(page_text.split()).lower()
            text += cleaned_text + "\n"
    return text
           

def process_pdfs_and_save_combined(files):
    all_text = []
    for file in files:
        if file.filename.endswith('.pdf'):
            candidate_text = pdf_to_text(file)
        elif file.filename.endswith('.docx'):
            candidate_text = docx_to_text(file)
        else:
            continue  # Skip unsupported file types
        all_text.append(candidate_text)
    return "\n".join(all_text)
