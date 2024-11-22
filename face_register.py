import cv2
import face_recognition
import pickle
import os
import numpy as np

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
print("Press 'r' to capture and register a new face, or 'q' to quit.")

# Variables for performance optimization
frame_resize_ratio = 0.5  # Scale down for faster processing
process_frame_interval = 5  # Process every 5 frames
frame_count = 0

while True:
    # Capture a single frame
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture image")
        break

    # Flip the frame to mirror it
    mirrored_frame = cv2.flip(frame, 1)
    small_frame = cv2.resize(mirrored_frame, (0, 0), fx=frame_resize_ratio, fy=frame_resize_ratio)

    # Only process every nth frame
    if frame_count % process_frame_interval == 0:
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        matches_found = []
        for face_encoding in face_encodings:
            match = None
            for name, encoding in known_faces.items():
                matches = face_recognition.compare_faces([encoding], face_encoding, tolerance=0.6)
                if matches[0]:
                    match = name
                    break
            matches_found.append(match)

    # Draw boxes and labels
    for (top, right, bottom, left), match in zip(face_locations, matches_found):
        # Scale back up face locations
        top = int(top / frame_resize_ratio)
        right = int(right / frame_resize_ratio)
        bottom = int(bottom / frame_resize_ratio)
        left = int(left / frame_resize_ratio)

        # Draw a box around the face
        color = (0, 255, 0) if match else (0, 0, 255)
        cv2.rectangle(mirrored_frame, (left, top), (right, bottom), color, 2)

        # Label the face as "Already Registered" or "Not Registered"
        label = f"Already Registered" if match else "Not Registered"
        cv2.putText(mirrored_frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Display the frame with face boxes and labels
    cv2.imshow('Register Face', mirrored_frame)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # If 'c' is pressed, capture and register the face
    if key == ord('r') and len(face_encodings) == 1:
        face_encoding = face_encodings[0]
        if not matches_found[0]:  # Not registered
            name = input("Enter the person's name: ")
            known_faces[name] = face_encoding
            print(f"Face registered for {name}.")
        else:
            print(f"Face is already registered.")

    # If 'q' is pressed, exit the loop
    elif key == ord('q'):
        break

    frame_count += 1  # Update frame count

# Release the webcam and close the window
video_capture.release()
cv2.destroyAllWindows()

# Save the updated encodings to a file
with open(encodings_file, 'wb') as f:
    pickle.dump(known_faces, f)

print("All faces have been saved to face_encodings.pkl")
