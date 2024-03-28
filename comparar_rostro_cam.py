import cv2
import face_recognition
import os

# Función para cargar y codificar las imágenes de la carpeta
def cargar_imagenes(carpeta):
    encodings = []
    nombres_imagenes = []
    for nombre_imagen in os.listdir(carpeta):
        ruta_imagen = os.path.join(carpeta, nombre_imagen)
        imagen = face_recognition.load_image_file(ruta_imagen)
        encoding = face_recognition.face_encodings(imagen)
        if encoding:  # Verificar si se encontraron rostros en la imagen
            encodings.append(encoding[0])
            nombres_imagenes.append(nombre_imagen)
        else:
            os.remove(ruta_imagen)  # Eliminar la imagen si no se detectan rostros
    return encodings, nombres_imagenes

# Carpeta que contiene las imágenes a comparar
carpeta_imagenes = "rostros"
encodings_carpeta, nombres_imagenes = cargar_imagenes(carpeta_imagenes)

# Iniciar la captura de video desde la cámara
cap = cv2.VideoCapture(0)

while True:
    # Capturar un frame de la cámara
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir el fotograma a RGB (face_recognition trabaja con imágenes en RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar rostros en el fotograma
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Comparar cada rostro detectado con las imágenes de la carpeta
    for encoding in face_encodings:
        coincidencias = face_recognition.compare_faces(encodings_carpeta, encoding)
        if any(coincidencias):
            indice = coincidencias.index(True)
            print(f"¡Coincidencia encontrada con {nombres_imagenes[indice]}!")
        else:
            print("No se encontraron coincidencias.")

    # Dibujar un rectángulo alrededor de cada rostro detectado
    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)

    # Mostrar el frame en una ventana
    cv2.imshow('Video de la cámara', frame)

    # Esperar 1 milisegundo y verificar si se presionó la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar la ventana
cap.release()
cv2.destroyAllWindows()