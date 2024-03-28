import cv2
import face_recognition
import os

# Carpeta que contiene las imágenes de rostros
carpeta_imagenes = "rostros"

# Obtener la lista de nombres de archivo de imágenes en la carpeta
nombres_imagenes = os.listdir(carpeta_imagenes)

# Cargar las imágenes y detectar rostros en cada una
for nombre_imagen in nombres_imagenes:
    # Leer la imagen
    ruta_imagen = os.path.join(carpeta_imagenes, nombre_imagen)
    imagen = cv2.imread(ruta_imagen)

    # Convertir la imagen a RGB (face_recognition trabaja con imágenes en RGB)
    rgb_imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    # Detectar rostros en la imagen
    face_locations = face_recognition.face_locations(rgb_imagen)

    # Dibujar un rectángulo alrededor de cada rostro detectado
    for top, right, bottom, left in face_locations:
        cv2.rectangle(imagen, (left, top), (right, bottom), (0, 255, 0), 2)

    # Mostrar la imagen con los rostros detectados
    cv2.imshow(f'Rostros en {nombre_imagen}', imagen)
    cv2.waitKey(0)  # Esperar hasta que se presione cualquier tecla para mostrar la siguiente imagen

# Cerrar todas las ventanas al finalizar
cv2.destroyAllWindows()
