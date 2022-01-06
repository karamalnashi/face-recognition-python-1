import face_recognition as fr
import face_recognition
import cv2
import os
from imutils import paths
from PIL import Image, ImageDraw
import numpy as np
import base64
import pickle

# Load test image to find faces in

new=True
embeddings ='./embeddings.pickle'
def get_encoded_faces():
    
    encoded = {}
    
    for dirpath, dnames, fnames in os.walk("./known"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("./known/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
                f = open(embeddings, "wb")
                f.write(pickle.dumps(encoded))
                f.close()
    return encoded


def unknown_image_encoded(img):
    """
    encode a face given the file name
    """
    face = fr.load_image_file("./known/" + img)
    encoding = fr.face_encodings(face)[0]
    get_encoded_faces()
    return encoding


def classify_face(im):

    
    faces = pickle.loads(open(embeddings, "rb").read())
    #faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
    #img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    #img = img[:,:,::-1]
 
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            cv2.rectangle(img, (left , top), (right, bottom), (255, 0, 0), 2)

            # Draw a label with a name below the face
           # cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(img, name, (left  , bottom +10 ), font, 2, (0, 0, 255),2)
            cv2.imwrite('identify.jpg', img )
    # Display the resulting image

#print(classify_face("test.jpg"))