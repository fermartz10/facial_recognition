import cv2
import face_recognition
from conexion import conexion_base, agregar_rostro, crear_tabla, consultar_base_datos, obtener_ultimo_id

# Inicializar la captura de video desde la cámara
video_capture = cv2.VideoCapture(0)

# Establecer la conexión a la base de datos
conexion, cursor = conexion_base()

# Crear la tabla si no existe
crear_tabla()

# Obtener el último ID registrado en la base de datos
ultimo_id = obtener_ultimo_id(cursor) or 0

# Inicializar el contador de frames
frame_count = 0

# Obtener los encodings de los rostros ya registrados en la base de datos
known_face_encodings = list(consultar_base_datos(cursor).values())

while True:
    # Capturar un frame del video
    ret, frame = video_capture.read()

     # Incrementar el contador de frames
    frame_count += 1

    # Procesar solo cada n-ésimo frame
    if frame_count % 10 == 0:  # Cambia el número 5 por el valor de n que desees
        # Convertir el frame a RGB (Face Recognition usa RGB)
    
        # Convertir el frame a RGB (Face Recognition usa RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectar ubicaciones de rostros en el frame
        face_locations = face_recognition.face_locations(rgb_frame)
        if face_locations:
            # Dibujar un cuadro alrededor de cada rostro detectado
            for top, right, bottom, left in face_locations:
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
                imagen_recortada = frame[max(0, top):min(rgb_frame.shape[0], bottom), max(0, left):min(rgb_frame.shape[1], right)]

                # Redimensionar la imagen recortada a un tamaño manejable
                nuevo_ancho = 200
                nuevo_alto = 200
                imagen_redimensionada = cv2.resize(imagen_recortada, (nuevo_ancho, nuevo_alto))

                # Convertir la imagen redimensionada a bytes para almacenarla en la base de datos
                imagen_bytes = cv2.imencode('.jpg', imagen_redimensionada)[1].tobytes()

                # Obtener el encoding del rostro
                face_encoding = face_recognition.face_encodings(rgb_frame, [(top, right, bottom, left)])[0]

                # Verificar si el rostro ya está registrado en la base de datos
                if any(face_recognition.compare_faces(known_face_encodings, face_encoding)):
                    print("El rostro ya está registrado.")
                    # Dibujar un cuadro verde alrededor del rostro
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
                else:
                    # Incrementar el ID para el nuevo rostro
                    nuevo_id = ultimo_id + 1

                    # Generar nombre con ID
                    nombre = f"Rostro{nuevo_id}"

                    # Convertir el encoding a una cadena de caracteres
                    encoding_str = ','.join(map(str, face_encoding))

                    # Agregar el rostro a la base de datos
                    agregar_rostro(nombre, encoding_str, imagen_bytes)

                    # Actualizar el último ID
                    ultimo_id = nuevo_id

                    # Agregar el nuevo encoding a la lista de encodings conocidos
                    known_face_encodings.append(face_encoding)

                    print("Se ha registrado un nuevo rostro.")
                    # Dibujar un cuadro azul alrededor del rostro
                    cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 1)

        # Mostrar el frame en una ventana
        cv2.imshow('Video', frame)

    # Si se presiona la tecla 'q', salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar las ventanas
video_capture.release()
cv2.destroyAllWindows()

# Cerrar la conexión a la base de datos
conexion.close()