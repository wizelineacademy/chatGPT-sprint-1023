#!/usr/bin/env python3

import json
from docx import Document
from io import BytesIO
from PyPDF2 import PdfReader
from brain_module import ChatGPT
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, static_folder='static')
bot = ChatGPT()

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/tailor', methods=['POST'])
def tailor():
    print("Received request")
    cv_file = request.files.get('cv')
    jobdesc_file = request.files.get('jobdesc')


    if cv_file and jobdesc_file:
        # Read the CV and job description files
        cv_text = decodeFile(cv_file)
        jobdesc_text = decodeFile(jobdesc_file)
        try:
            # Prompt the chatbot with the CV and job description
            response = bot.prompt(cv_text, jobdesc_text)
        except:
            # If the chatbot fails, return an error message
            response = "An error occurred while processing the CV and job description."
        # Sanitize the response
        json_response = sanitize(response)
        if 'error' in json_response:
            return json_response['error'], 400
        return render_tailored_cv(json_response)
    else:
        return "No file(s) uploaded", 400
    
def sanitize(message):
    # The message is a JSON string wrapped in backticks
    # like: ```json\n{...}\n``` so we need to remove them
    message = message.replace('```json\n', '')
    message = message.replace('\n```', '')
    # Parse the JSON string into a Python dictionary
    try:
        message = json.loads(message)
        # Ensure that the message follows JSON Resume schema
        resume_schema = [
            'basics',
            'work',
            'education',
            'skills',
            'jobDescriptionAlignment',
        ]
        # Ensure that the message contains the job description
        job_schema = [
            'title',
            'description',
            'company',
        ]
        valid = False
        
        if all(key in message for key in resume_schema):
            valid = all(key in message['job'] for key in job_schema)
        if not valid:
            message = {"error": "The response from the chatbot was not valid."}
    except json.decoder.JSONDecodeError as e:
        print(">>>JSONDecodeError", e, "<<<JSONDecodeError")
        print(">>>message", message, "<<<message")
        message = {"error": "An error occurred while processing the CV and job description."}
    return message
    
def render_tailored_cv(data):
    print("Rendering tailored CV")
    print(data)
    template_file = 'tailored_cv.html'
    template_data = {
        'basics': data['basics'],
        'work': data['work'],
        'education': data['education'],
        'skills': data['skills'],
        'jobDescriptionAlignment': data['jobDescriptionAlignment'],
        'job': data['job']
    }
    return render_template(template_file, **template_data)

def decodeFile(file):
    """
    Decode a file into a string.
    
    Accepted MIME types: .pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, text/plain
    """
    # Read the file
    file_content = file.read()

    # Check the file type
    if file.content_type == 'application/pdf':
        # Decode the PDF file
        reader = PdfReader(BytesIO(file_content))
        text = ' '.join(page.extract_text() for page in reader.pages)
    elif file.content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        # Decode the Word document
        doc = Document(BytesIO(file_content))
        text = ' '.join(paragraph.text for paragraph in doc.paragraphs)
    else:
        # Decode the text file
        text = file_content.decode('utf-8')

    return text

if __name__ == "__main__":
    app.run(port=5000)