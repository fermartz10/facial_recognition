import cv2
import face_recognition
import os

# Crear un directorio para guardar las capturas
os.makedirs("capturas", exist_ok=True)

# Iniciar la captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Contador para el nombre de las capturas
capture_count = len(os.listdir("capturas"))

while True:
    # Leer un fotograma del video
    ret, frame = cap.read()

    if not ret:
        break

    # Hacer una copia del fotograma original para guardar sin el rectángulo
    frame_original = frame.copy()

    # Convertir el fotograma a RGB (face_recognition trabaja con imágenes en RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar rostros en el fotograma
    face_locations = face_recognition.face_locations(rgb_frame)

    # Dibujar un rectángulo alrededor de cada rostro detectado
    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)

        # Guardar una captura si se detecta un rostro
        capture_path = os.path.join("capturas", f"capture_{capture_count}.jpg")
        cv2.imwrite(capture_path, frame_original)#frame_original para guardar sin cuadro
        print(f"Captura guardada: {capture_path}")
        capture_count += 1

    # Mostrar el fotograma con los rostros detectados
    cv2.imshow('Video con rostros detectados', frame)

    # Romper el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()

