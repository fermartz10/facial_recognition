import cv2
import numpy as np
import mysql.connector

def mostrar_imagen_rostro(cursor):
    try:
        # Consultar la base de datos para obtener el ID, el nombre y la imagen del rostro
        cursor.execute("SELECT id, nombre, imagen FROM caras")
        rostros = cursor.fetchall()

        # Mostrar cada rostro
        for id, nombre, imagen_blob in rostros:
            # Decodificar la imagen BLOB
            nparr = np.frombuffer(imagen_blob, np.uint8)
            imagen_decodificada = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Mostrar la imagen con el ID y el nombre
            cv2.imshow(f"ID: {id}, Nombre: {nombre}", imagen_decodificada)

        # Esperar a que se presione una tecla para cerrar las ventanas
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except mysql.connector.Error as err:
        print("Error al obtener los datos de la base de datos:", err)


# Establecer la conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="base_rostros"
)
cursor = conexion.cursor()

# Llamar a la función para mostrar las imágenes de los rostros
mostrar_imagen_rostro(cursor)

# Cerrar la conexión a la base de datos
cursor.close()
conexion.close()
