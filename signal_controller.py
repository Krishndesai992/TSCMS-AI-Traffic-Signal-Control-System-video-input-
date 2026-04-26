import time
import config


class SignalController:

    def __init__(self, lanes):
        self.lanes = lanes  # dynamic lanes
        self.current_index = 0

        self.green_time = config.GREEN_TIME
        self.yellow_time = config.YELLOW_TIME

        self.state = "GREEN"
        self.start_time = time.time()

    def update(self):
        elapsed = time.time() - self.start_time

        if self.state == "GREEN" and elapsed >= self.green_time:
            self.state = "YELLOW"
            self.start_time = time.time()

        elif self.state == "YELLOW" and elapsed >= self.yellow_time:
            self.state = "GREEN"
            self.current_index = (self.current_index + 1) % len(self.lanes)
            self.start_time = time.time()

    # ✅ Apply dynamic timing ONLY when NEW GREEN starts
    def set_green_time(self, new_time):

        # detect new cycle
        if self.state == "GREEN" and int(time.time() - self.start_time) == 0:
            self.green_time = new_time

    def get_current_lane(self):
        return self.lanes[self.current_index]

    def get_state(self):
        return self.state

    def get_timer(self):
        elapsed = time.time() - self.start_time

        if self.state == "GREEN":
            return max(0, int(self.green_time - elapsed))
        else:
            return max(0, int(self.yellow_time - elapsed))