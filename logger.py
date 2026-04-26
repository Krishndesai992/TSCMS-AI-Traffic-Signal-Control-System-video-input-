import os
from datetime import datetime


class Logger:

    def __init__(self, log_file="logs/traffic_log.txt"):
        os.makedirs("logs", exist_ok=True)
        self.log_file = log_file

    def log(self, vehicle_count, density, signal_time, emergency):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = f"Vehicles: {vehicle_count}, Density: {density}, SignalTime: {signal_time}, Emergency: {emergency}"

        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")