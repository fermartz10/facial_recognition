import cv2
import face_recognition
from conexion import conexion_base, agregar_rostro, crear_tabla, obtener_ultimo_id

# Inicializar la captura de video desde la cámara
video_capture = cv2.VideoCapture(0)

conexion, cursor = conexion_base()
# Crear la tabla si no existe
crear_tabla()

# Obtener el último ID registrado en la base de datos
ultimo_id = obtener_ultimo_id(cursor) or 0

while True:
    # Capturar un frame del video
    ret, frame = video_capture.read()

    # Convertir el frame a RGB (Face Recognition usa RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar ubicaciones de rostros en el frame
    face_locations = face_recognition.face_locations(rgb_frame)

    if face_locations:
        # Tomar la primera cara detectada (asumimos que solo hay una cara en el frame)
        top, right, bottom, left = face_locations[0]

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

        # Convertir el encoding a una cadena de caracteres
        encoding_str = ','.join(map(str, face_encoding))
        
        # Incrementar ID para el nuevo rostro
        nuevo_id = ultimo_id + 1
        
        # Generar nombre con ID
        nombre = f"Rostro{nuevo_id}"

        # Agregar el rostro a la base de datos
        agregar_rostro(nombre, encoding_str, imagen_bytes)

        # Actualizar el último ID
        ultimo_id = nuevo_id

        # Mostrar el frame con un cuadro alrededor de la cara
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Mostrar el frame en una ventana
    cv2.imshow('Video', frame)

    # Si se presiona la tecla 'q', salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar las ventanas
video_capture.release()
cv2.destroyAllWindows()
