import mysql.connector
import numpy as np
from datetime import datetime
import cv2

def conexion_base():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='base_rostros'
        )
        cursor = conexion.cursor()
        return conexion, cursor
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos:", err)
        return None, None

def crear_tabla():
    try:
        conexion, cursor = conexion_base()
        cursor.execute("CREATE TABLE IF NOT EXISTS caras (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), encoding TEXT, imagen BLOB, fecha_hora DATETIME)")
        conexion.close()
    except mysql.connector.Error as err:
        print("Error al crear la tabla en la base de datos:", err)

def consultar_base_datos(cursor):    
    try:
        cursor.execute("SELECT nombre, encoding FROM caras")
        rows = cursor.fetchall()
        known_faces = {nombre: np.fromstring(encoding, sep=',') for nombre, encoding in rows}
        return known_faces
    except mysql.connector.Error as err:
        print("Error al consultar la base de datos:", err)
        return {}

def obtener_ultimo_id(cursor):
    try:
        cursor.execute("SELECT MAX(id) FROM caras")
        ultimo_id = cursor.fetchone()[0]
        return ultimo_id if ultimo_id is not None else 0
    except mysql.connector.Error as err:
        print("No se pudo obtener el último id", err)
        
def agregar_rostro(nombre, encoding_str, imagen_bytes):
    try:
        conexion, cursor = conexion_base()
        cursor.execute("INSERT INTO caras (nombre, encoding, imagen, fecha_hora) VALUES (%s, %s, %s, %s)", (nombre, encoding_str, imagen_bytes, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conexion.commit()
        conexion.close()
        print("Se agrego el rostro correctamente", nombre)
    except mysql.connector.Error as err:
        print("Error al agregar rostro a la base de datos:", err)
        
def eliminar_rostro(nombre):
    try:
        conexion, cursor = conexion_base()
        cursor.execute("DELETE FROM caras WHERE nombre = %s", (nombre,))
        cursor._connection.commit()
        print("Rostros eliminados correctamente.")
    except mysql.connector.Error as err:
        print("Error al eliminar rostros ", err)

def cerrar_conexion(conexion):
    try:
        conexion.close()
    except mysql.connector.Error as err:
        print("Error al cerrar la conexión a la base de datos:", err)
        
def obtener_id_por_nombre(cursor, nombre):
    try:
        cursor.execute("SELECT id FROM caras WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
    except mysql.connector.Error as err:
        print("No se pudo obtener el id por nombre", err)
    
def obtener_rostros(cursor):
    try:
        cursor.execute("SELECT nombre, imagen FROM caras")
        resultados = cursor.fetchall()
        rostros = []
        for nombre, imagen_bytes in resultados:
            # Convertir la imagen de bytes a matriz numpy
            imagen_np = np.frombuffer(imagen_bytes, np.uint8)
            # Decodificar la imagen 
            imagen = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)
            rostros.append((nombre,imagen))
            return rostros
    except mysql.connector.Error as err:
        print("Error al obtener los rostros de la base de datos", err)
        return []
    
   
