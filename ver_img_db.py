import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="base_rostros"
)

cursor = conexion.cursor()

# Seleccionar la imagen con el id correspondiente
cursor.execute("SELECT imagen FROM caras WHERE id = 42")
imagen_bytes = cursor.fetchone()[0]

# Guardar la imagen como un archivo
with open('imagen_f.jpg', 'wb') as archivo:
    archivo.write(imagen_bytes)

conexion.close()
