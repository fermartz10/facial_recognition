import cv2
from ultralytics import YOLO

# Cargar el modelo YOLO preentrenado para detección de objetos
object_model = YOLO('armas.pt')

# Cargar el modelo YOLO preentrenado para detección de poses
pose_model = YOLO('yolov8n-pose.pt')

# Función para detectar objetos y poses en una imagen
def detect_objects_and_pose(image, object_model, pose_model, confidence_threshold=0.5):
    # Detectar objetos en la imagen
    object_results = object_model(image)[0]
    
    # Detectar poses en la imagen
    pose_results = pose_model(image)[0]
    
    # Dibujar cuadros delimitadores y nombres de clases para objetos detectados
    for result in object_results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score >= confidence_threshold:
            class_name = object_results.names[int(class_id)]
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(image, class_name, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Dibujar cuadros delimitadores para poses detectadas
    for result in pose_results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score >= confidence_threshold:
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

    # Retorna la imagen modificada
    return image

# Cargar una imagen desde un archivo
image_path = 'cuchillo1.png'  # Ruta al archivo de imagen
image = cv2.imread(image_path)

# Detectar objetos y poses en la imagen
image_with_detections = detect_objects_and_pose(image, object_model, pose_model, confidence_threshold=0.3)

# Mostrar la imagen con las detecciones
cv2.imshow('Detecciones en imagen', image_with_detections)

# Esperar a que se presione una tecla para cerrar la ventana
cv2.waitKey(0)
cv2.destroyAllWindows()
