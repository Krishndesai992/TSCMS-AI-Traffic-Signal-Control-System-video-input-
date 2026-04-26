from ultralytics import YOLO


class YOLODetector:

    def __init__(self):
        self.model = YOLO("yolov8n.pt")
        self.vehicle_classes = [2, 3, 5, 7]

    def detect(self, frame):

        results = self.model(frame, stream=True)

        detections = []

        for r in results:
            for box in r.boxes:

                cls = int(box.cls[0])

                if cls in self.vehicle_classes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    detections.append([x1, y1, x2, y2])

        return detections