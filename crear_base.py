import mysql.connector
import face_recognition
import cv2
from datetime import datetime
from conexion import conexion_base

conexion, cursor = conexion_base()

# Crear la base de datos si no existe
cursor.execute("CREATE DATABASE IF NOT EXISTS base_rostros")

# Seleccionar la base de datos
conexion.database = "base_rostros"

# Diccionario de caras reconocidas
known_faces = {
    #"Ben": face_recognition.face_encodings(face_recognition.load_image_file("capturas/ben.jpg"))[0],
    "Fernando": face_recognition.face_encodings(face_recognition.load_image_file("capturas/fernando.jpg"))[0],
   # "Keanu": face_recognition.face_encodings(face_recognition.load_image_file("capturas/keanu.jpg"))[0],
}

# Crear la tabla si no existe
cursor.execute("CREATE TABLE IF NOT EXISTS caras (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), encoding TEXT, imagen BLOB, fecha_hora DATETIME)")

for nombre, encoding in known_faces.items():
    # Cargar la imagen original
    imagen_original = face_recognition.load_image_file(f"capturas/{nombre.lower()}.jpg")
    
    # Detectar ubicaciones de rostros en la imagen original
    face_locations = face_recognition.face_locations(imagen_original)
    
    # Obtener las coordenadas de la región de interés (ROI) que rodea el rostro
    top, right, bottom, left = face_locations[0]  # Suponemos que solo hay un rostro en la imagen
    
    # Calcular la ampliación del 20%
    width = right - left
    height = bottom - top
    ampliacion = int(0.20 * max(width, height))
    
    # Ampliar la región de interés (ROI) para incluir un 20% más en todas las direcciones
    top -= ampliacion
    right += ampliacion
    bottom += ampliacion 
    left -= ampliacion
    
    # Recortar la región de interés (ROI) de la imagen original
    imagen_recortada = imagen_original[max(0, top):min(imagen_original.shape[0], bottom), max(0, left):min(imagen_original.shape[1], right)]

    # Redimensionar la imagen recortada a un tamaño manejable
    nuevo_ancho = 200
    nuevo_alto = 200
    imagen_redimensionada = cv2.resize(imagen_recortada, (nuevo_ancho, nuevo_alto))

    # Convertir la imagen redimensionada a bytes para almacenarla en la base de datos
    imagen_bytes = cv2.imencode('.jpg', imagen_redimensionada)[1].tobytes()

    # Convertir el encoding a una cadena de caracteres
    encoding_str = ','.join(map(str, encoding))

    # Obtener la fecha y hora actual
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insertar los datos en la tabla
    cursor.execute("INSERT INTO caras (nombre, encoding, imagen, fecha_hora) VALUES (%s, %s, %s, %s)", (nombre, encoding_str, imagen_bytes, fecha_hora))

# Confirmar los cambios en la base de datos
conexion.commit()

# Cerrar la conexión
conexion.close()

#crear la base con los rostros que va detectando, despues hacer 
# la comparativa con los nuevos para que no guarde repetidos 
#pero primero debe guardar rostros a la base