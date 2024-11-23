Follow these steps to run the FaceRac project:

1. Install Python 3 (3.8 or later)

2. Run the following command to install dependencies:
	>>> pip install face_recognition opencv-python numpy

  # Required Libraries:
	> face_recognition
	> opencv-python
	> numpy
	> pickle

3.Verify Installation of dependencies using the following command
	>>> python3 -c "import cv2, face_recognition, numpy; print('All libraries installed successfully!')"

4. Unzip FaceRec.zip 

5. Open the FaceRec Directory in VS-Code

6. Run Main_ui.py file.

7. Click on "Register Face" button to register your face using webcam.
	> enter Admin Password : "superhero"
	> once webcam sees you, press "r" key, then enter your name in VS.code command prompt. (your face encodings will be saved against your name in an encodings file.)

8. Click on "Authenticate Face" button to perform user authentication, user will only pass the authentication screen if he/she is registered.
