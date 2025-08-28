

from flask import Flask, request, jsonify, send_from_directory
import os

# Initialize the Flask application
app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    """
    Serves the main HTML file of the application.
    """
    # Assumes your HTML file is named 'index.html' and is in the same directory
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles the file upload POST request from the frontend.
    Extracts file metadata and returns it as JSON.
    """
    # Check if the 'file' part is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # Check if a file was actually selected by the user
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        # Get the filename
        filename = file.filename
        
        # Get the file type (MIME type)
        file_type = file.mimetype
        
        # Calculate the file size in kilobytes
        # Move cursor to the end of the file to get its size
        file.seek(0, os.SEEK_END)
        file_size_bytes = file.tell()
        file_size_kb = round(file_size_bytes / 1024, 2)

        # Prepare the response data
        response_data = {
            'filename': filename,
            'size_kb': file_size_kb,
            'type': file_type
        }
        
        # Return the data as a JSON response
        return jsonify(response_data), 200

    # Fallback error case
    return jsonify({'error': 'An unknown error occurred'}), 500

if __name__ == '__main__':
    # Runs the app in debug mode for development
    app.run(debug=True)
