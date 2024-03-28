import os
import face_recognition

# Cargar la imagen de referencia (el rostro que quieres comparar)
imagen_referencia = face_recognition.load_image_file("capturas/capture_11.jpg")

# Detectar rostros en la imagen de referencia
face_locations_referencia = face_recognition.face_locations(imagen_referencia)
encodings_referencia = face_recognition.face_encodings(imagen_referencia, face_locations_referencia)

# Carpeta que contiene las imágenes a comparar
carpeta_imagenes = "rostros"

# Lista para almacenar los resultados de la comparación
resultados_comparacion = {}

# Iterar sobre todas las imágenes en la carpeta
for nombre_imagen in os.listdir(carpeta_imagenes):
    ruta_imagen = os.path.join(carpeta_imagenes, nombre_imagen)
    imagen_a_comparar = face_recognition.load_image_file(ruta_imagen)

    # Detectar y codificar los rostros en la imagen a comparar
    face_locations_a_comparar = face_recognition.face_locations(imagen_a_comparar)
    encodings_a_comparar = face_recognition.face_encodings(imagen_a_comparar, face_locations_a_comparar)

    # Comparar cada rostro en la imagen a comparar con los rostros en la imagen de referencia
    resultados_por_imagen = []
    for encoding_a_comparar in encodings_a_comparar:
        distancias = face_recognition.face_distance(encodings_referencia, encoding_a_comparar)
        resultado = min(distancias) < 0.6  # Usar un umbral de distancia para determinar si los rostros son iguales
        resultados_por_imagen.append(resultado)

    # Guardar los resultados de la comparación para esta imagen
    resultados_comparacion[os.path.splitext(nombre_imagen)[0]] = resultados_por_imagen

# Imprimir los resultados de la comparación
for nombre_imagen, resultados in resultados_comparacion.items():
    if any(resultados):
        print(f"Coincidencia encontrada en {nombre_imagen}")
    else:
        print(f"No se encontró coincidencia en {nombre_imagen}")
