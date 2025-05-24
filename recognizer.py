import face_recognition
import os
import numpy as np

# Load known faces from a folder
def load_known_faces(known_dir="known_faces"):
    known_encodings = []
    known_names = []

    for file in os.listdir(known_dir):
        path = os.path.join(known_dir, file)
        img = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(file)[0])
    return known_encodings, known_names

# Detect and recognize faces in a given image
def recognize_faces(image_path, known_encodings, known_names, tolerance=0.45):
    img = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    results = []
    for face_encoding in face_encodings:
        distances = face_recognition.face_distance(known_encodings, face_encoding)

        if len(distances) == 0:
            results.append("Unknown")
            continue

        best_match_index = np.argmin(distances)
        if distances[best_match_index] < tolerance:
            results.append(known_names[best_match_index])
        else:
            results.append("Unknown")

    return results
