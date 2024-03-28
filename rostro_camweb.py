import cv2
import numpy as np
import face_recognition
from PIL import Image, ImageDraw, ImageFont

# Define las codificaciones faciales y los nombres de las caras de referencia
known_faces = {
    "Ben": face_recognition.face_encodings(face_recognition.load_image_file("capturas/ben.jpg"))[0],
    "Fernando": face_recognition.face_encodings(face_recognition.load_image_file("capturas/capture_7.jpg"))[0],
    "Keanu": face_recognition.face_encodings(face_recognition.load_image_file("capturas/keanu.jpg"))[0],
}

# Inicializa las variables para el video en tiempo real
video_capture = cv2.VideoCapture(0)

while True:
    # Captura un frame del video
    ret, frame = video_capture.read()

    # Encuentra las ubicaciones y codificaciones de las caras en el frame actual
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Inicializa las listas para los nombres de las caras detectadas
    face_names = []

    # Compara cada cara detectada con las caras de referencia conocidas
    for face_encoding in face_encodings:
        # Compara la cara actual con todas las caras de referencia
        matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
        name = "Desconocido"

        # Encuentra el nombre correspondiente a la mejor coincidencia
        if True in matches:
            first_match_index = matches.index(True)
            name = list(known_faces.keys())[first_match_index]

        face_names.append(name)

    # Dibuja cuadros y etiquetas alrededor de las caras detectadas en el frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Dibuja un cuadro alrededor de la cara
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Dibuja una etiqueta con el nombre de la cara debajo del cuadro
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Muestra el frame con las caras detectadas y sus etiquetas
    cv2.imshow('Video', frame)

    # Si se presiona la tecla 'q', salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos y cierra las ventanas
video_capture.release()
cv2.destroyAllWindows()
