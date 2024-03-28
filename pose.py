def detector_pose():   
    from ultralytics import YOLO
    model = YOLO ('yolov8n-pose.pt')
    results = model(source = 0, show= True, conf = 0.3)

detector_pose()


'''Como resolución de cámara predeterminada, su navegador utiliza 640×480 (0.307MP).
        La resolución máxima admitida de su cámara es 1280×720 (0.922MP).'''

