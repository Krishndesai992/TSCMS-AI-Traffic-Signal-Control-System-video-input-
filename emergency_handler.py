class EmergencyHandler:

    def detect(self, detections):

        if len(detections) > 20:
            return True

        return False