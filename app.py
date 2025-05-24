from flask import Flask, render_template, request, redirect, url_for, jsonify
from recognizer import recognize_faces, load_known_faces
from db import init_db, log_recognition
import os, base64, re, cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

init_db()
known_encodings, known_names = load_known_faces()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        results = recognize_faces(path, known_encodings, known_names)
        for name in results:
            log_recognition(name, "Upload")
        return render_template('index.html', result=results, image_path='images/' + file.filename)
    return redirect(url_for('index'))

@app.route('/capture_snapshot', methods=['POST'])
def capture_snapshot():
    data = request.get_json()
    img_data = re.sub('^data:image/.+;base64,', '', data['image'])
    img_bytes = base64.b64decode(img_data)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], "captured.jpg")
    with open(file_path, "wb") as f:
        f.write(img_bytes)

    results = recognize_faces(file_path, known_encodings, known_names)
    for name in results:
        log_recognition(name, "Camera")

    return jsonify({
        'result': results,
        'image_url': url_for('static', filename='images/captured.jpg')
    })

if __name__ == '__main__':
    app.run(debug=True)