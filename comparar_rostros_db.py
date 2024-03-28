import cv2
import face_recognition
from conexion import conexion_base, consultar_base_datos, obtener_id_por_nombre

conexion, cursor = conexion_base()

# Inicializa las variables para el video en tiempo real
video_capture = cv2.VideoCapture(0)

# Contador para controlar el intervalo de procesamiento
frame_count = 0
processing_interval = 5  # Procesar una imagen de cada 5 frames

while True:
    # Captura un frame del video
    ret, frame = video_capture.read()
    frame_count += 1

    if ret and frame_count % processing_interval == 0:
        # Convertir el frame a RGB (Face Recognition usa RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectar ubicaciones de rostros en el frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Inicializa las listas para los nombres de las caras detectadas
        face_names = []

        known_faces = consultar_base_datos(cursor)
        
        # Compara cada cara detectada con las caras de referencia conocidas
        for face_encoding in face_encodings:
            # Compara la cara actual con todas las caras de referencia
            matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
            name = "Desconocido"

            # Encuentra el nombre correspondiente a la mejor coincidencia
            if True in matches:
                first_match_index = matches.index(True)
                name = list(known_faces.keys())[first_match_index]

            face_names.append(name)

        # Dibuja cuadros y etiquetas alrededor de las caras detectadas en el frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Dibuja un cuadro alrededor de la cara
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
            
            #Obtener id de la base de datos
            id_rostro = obtener_id_por_nombre (cursor, name) if name != 'Desconocido' else None
            
            #Si se encontro el Id, se muesta el Id en la etiqueta 
            if id_rostro:
                # Dibuja una etiqueta con el nombre de la cara debajo del cuadro
                cv2.putText(frame, f"ID: {id_rostro}", (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
            else: # si no encontro el Id muestra el nombre
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        # Muestra el frame con las caras detectadas y sus etiquetas
        cv2.imshow('Video', frame)

    # Si se presiona la tecla 'q', salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar las ventanas
video_capture.release()
cv2.destroyAllWindows()

# Cerrar la conexión a la base de datos al finalizar
conexion.close()