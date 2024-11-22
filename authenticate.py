import cv2
import face_recognition
import pickle
import os
import sys
import time
from tkinter import messagebox

# Path to save the encodings
encodings_file = 'face_encodings.pkl'

# Load existing encodings if available
if os.path.exists(encodings_file):
    with open(encodings_file, 'rb') as f:
        known_faces = pickle.load(f)
else:
    known_faces = {}  # Initialize an empty dictionary

# Open the webcam
video_capture = cv2.VideoCapture(0)

start_time = time.time()
recognized = False

while True:
    # Capture a single frame
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture image")
        break

    # Flip the frame to mirror it
    mirrored_frame = cv2.flip(frame, 1)

    # Detect face locations and encodings in the frame
    face_locations = face_recognition.face_locations(mirrored_frame)
    face_encodings = face_recognition.face_encodings(mirrored_frame, face_locations)

    # Iterate over each detected face
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if face is already registered
        match = None
        for name, encoding in known_faces.items():
            matches = face_recognition.compare_faces([encoding], face_encoding, tolerance=0.6)
            if matches[0]:
                match = name
                recognized = True
                break

        # Draw a box around the face
        cv2.rectangle(mirrored_frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Label the face as "Known" or "Unknown"
        label = match if match else "Unknown"

        # Display the label text above the bounding box
        cv2.putText(mirrored_frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the frame with face boxes and labels
    cv2.imshow('Face Recognition', mirrored_frame)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # If 'q' is pressed, exit the loop
    if key == ord('q'):
        break

    if recognized:
        break

    # Exit after 5 seconds if not recognized
    if time.time() - start_time > 5 and not recognized:
        print("Authentication timed out.")
        messagebox.showerror("Authentication", "Authentication timed out.")
        break

# Release the webcam and close the window
video_capture.release()
cv2.destroyAllWindows()

# Exit with code indicating whether a face was recognized
if recognized:
    sys.exit(0)  # Success
else:
    sys.exit(1)  # Failure
