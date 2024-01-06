from ultralytics import YOLO


class PlateDetector:
    def __init__(self, yolo_model_path):
        self.model = YOLO(yolo_model_path)

    def detect(self, image):
        results = self.model(image, verbose=False, classes=0, conf=0.3)
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        return boxes
