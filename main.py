import cv2
import time

from modules.yolo_detector import YOLODetector
from modules.vehicle_detector import VehicleDetector
from modules.timing_algorithm import TimingAlgorithm
from modules.signal_controller import SignalController
from modules.emergency_handler import EmergencyHandler
from modules.logger import Logger


VIDEO_PATH = "videos/traffic_sample.mp4"


def main():

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    yolo = YOLODetector()
    vehicle_detector = VehicleDetector()
    timing_algo = TimingAlgorithm()

    # ✅ ONLY 2 LANES (CHANGE HERE IF NEEDED)
    signal = SignalController(["Lane 1", "Lane 2"])

    emergency = EmergencyHandler()
    logger = Logger()

    print("System Started...\n")

    last_density_update = time.time()
    density = "LOW"

    while True:
        ret, frame = cap.read()

        if not ret:
            print("\nVIDEO FINISHED")
            print(f"TOTAL VEHICLES COUNTED: {vehicle_detector.get_total_count()}")
            break

        frame = cv2.resize(frame, (1020, 500))

        # COUNT LINE
        cv2.line(frame, (0, 250), (1020, 250), (0, 0, 255), 2)

        detections = yolo.detect(frame)

        vehicle_count = vehicle_detector.update(detections, frame)

        # ✅ Stable density update
        if time.time() - last_density_update > 3:
            density = timing_algo.calculate_density(vehicle_count)
            last_density_update = time.time()

        emergency_flag = emergency.detect(detections)

        signal_time = timing_algo.get_signal_time(density, emergency_flag)

        # ✅ APPLY dynamic timing properly
        signal.set_green_time(signal_time)

        signal.update()

        logger.log(vehicle_count, density, signal_time, emergency_flag)

        # 🔥 DISPLAY EVERYTHING CLEARLY
        cv2.putText(frame, f"Vehicles: {vehicle_detector.get_total_count()}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(frame, f"Density: {density}",
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.putText(frame, f"Signal: {signal.get_state()}",
                    (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        cv2.putText(frame, f"Active Lane: {signal.get_current_lane()}",
                    (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

        cv2.putText(frame, f"Timer: {signal.get_timer()}",
                    (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)

        # 🔥 SHOW DYNAMIC TIME (VERY IMPORTANT FOR DEMO)
        cv2.putText(frame, f"Assigned Green Time: {signal_time}",
                    (20, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 150, 255), 2)

        if emergency_flag:
            cv2.putText(frame, "EMERGENCY DETECTED!",
                        (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

        cv2.imshow("Traffic Control System", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()