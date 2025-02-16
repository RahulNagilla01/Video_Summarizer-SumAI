from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from video_summary import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Limit upload size to 500MB

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])

def summarize_video(video_path):
    audio_path = extract_audio(video_path)
    transcribed_text = transcribe_audio(audio_path)
    summary = summarize_text(transcribed_text)

    # Clean up the audio file
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return summary

def summarize():
    summary = None
    error = None

    # Check if a file was uploaded
    if 'video' in request.files:
        video_file = request.files['video']
        if video_file and video_file.filename != '':
            # Secure the filename and save the uploaded file
            filename = secure_filename(video_file.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video_file.save(video_path)

            try:
                # Generate summary
                summary = summarize_video(video_path)
            except Exception as e:
                error = f"An error occurred during summarization: {str(e)}"
            finally:
                # Remove the video file after processing
                if os.path.exists(video_path):
                    os.remove(video_path)
        else:
            error = "No video file selected."
    else:
        error = "No video file uploaded."

    if summary:
        return jsonify({'summary': summary})
    else:
        return jsonify({'error': error})

if __name__ == '__main__':
    app.run(debug=True)
