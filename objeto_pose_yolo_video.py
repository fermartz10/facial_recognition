import cv2
from ultralytics import YOLO

# Cargar el modelo YOLO preentrenado para detección de objetos
object_model = YOLO('armas.pt')

# Cargar el modelo YOLO preentrenado para detección de poses
pose_model = YOLO('yolov8n-pose.pt')

# Función para detectar objetos y poses en un fotograma
def detect_objects_and_pose(frame, object_model, pose_model, confidence_threshold=0.5):
    # Detectar objetos en el fotograma
    object_results = object_model(frame)[0]
    
    # Detectar poses en el fotograma
    pose_results = pose_model(frame)[0]
    
    # Dibujar cuadros delimitadores y nombres de clases para objetos detectados
    for result in object_results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score >= confidence_threshold:
            class_name = object_results.names[int(class_id)]
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, class_name, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Dibujar cuadros delimitadores para poses detectadas
    for result in pose_results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score >= confidence_threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

    # Retorna el fotograma modificado
    return frame

# Capturar video desde un archivo o la cámara
video_path = 0  # Ruta al archivo de video
cap = cv2.VideoCapture(video_path)

# Crear una ventana con capacidad de redimensionamiento
cv2.namedWindow('Detecciones en video', cv2.WINDOW_NORMAL)

while cap.isOpened():
    # Leer el fotograma actual
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Detectar objetos y poses en el fotograma
    frame_with_detections = detect_objects_and_pose(frame, object_model, pose_model, confidence_threshold=0.3)
    
    # Mostrar el fotograma con las detecciones
    cv2.imshow('Detecciones en video', frame_with_detections)
    
    # Romper el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()

