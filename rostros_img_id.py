import cv2
import face_recognition
import os
import json
import uuid

# Carpeta que contiene las imágenes de rostros
carpeta_imagenes = "capturas"

# Crear un directorio para guardar los rostros
os.makedirs("rostros", exist_ok=True)

# Nombre del archivo donde se guardarán los datos
archivo_datos = "rostros_info.json"

# Iterar sobre cada imagen en la carpeta
for nombre_imagen in os.listdir(carpeta_imagenes):
    ruta_imagen = os.path.join(carpeta_imagenes, nombre_imagen)

    # Leer la imagen
    frame = cv2.imread(ruta_imagen)

    # Convertir el fotograma a RGB (face_recognition trabaja con imágenes en RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar rostros en el fotograma
    face_locations = face_recognition.face_locations(rgb_frame)

    # Si se detecta al menos un rostro
    if face_locations:
        # Iterar sobre cada rostro detectado
        for idx, (top, right, bottom, left) in enumerate(face_locations):
            # Extraer la región del rostro
            face_image = frame[top:bottom, left:right]

            # Generar un ID único para el rostro
            face_id = uuid.uuid4().hex

            # Guardar la imagen del rostro
            face_path = os.path.join("rostros", f"rostro_{face_id}.jpg")
            cv2.imwrite(face_path, face_image)
            print(f"Rostro guardado: {face_path}")

            # Crear el diccionario de información del rostro
            face_info = {
                "ID": face_id,
                "Ubicacion": (top, right, bottom, left),
                # Agrega más información aquí según sea necesario
            }

            # Guardar face_info en el archivo JSON
            with open(archivo_datos, 'a') as file:
                json.dump(face_info, file)
                file.write('\n')

print("Proceso completado. Rostros guardados y archivo de información generado.")
