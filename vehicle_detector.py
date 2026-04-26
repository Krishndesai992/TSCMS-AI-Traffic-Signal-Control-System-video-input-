import math


class VehicleDetector:

    def __init__(self):
        self.next_id = 0
        self.objects = {}  # id -> centroid
        self.counted_ids = set()

        self.total_count = 0

        # Counting line (horizontal)
        self.line_y = 250
        self.offset = 15

    def _get_centroid(self, box):
        x1, y1, x2, y2 = box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        return (cx, cy)

    def _distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def update(self, detections, frame):

        new_objects = {}

        for box in detections:
            centroid = self._get_centroid(box)

            matched_id = None

            for obj_id, prev_centroid in self.objects.items():
                if self._distance(centroid, prev_centroid) < 50:
                    matched_id = obj_id
                    break

            if matched_id is None:
                matched_id = self.next_id
                self.next_id += 1

            new_objects[matched_id] = centroid

            # ✅ COUNT ONLY WHEN CROSSING LINE
            cx, cy = centroid

            if (self.line_y - self.offset) < cy < (self.line_y + self.offset):
                if matched_id not in self.counted_ids:
                    self.total_count += 1
                    self.counted_ids.add(matched_id)

        self.objects = new_objects

        return len(detections)

    def get_total_count(self):
        return self.total_count