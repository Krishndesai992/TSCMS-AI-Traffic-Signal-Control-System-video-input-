class TimingAlgorithm:

    def calculate_density(self, count):

        if count < 5:
            return "LOW"
        elif count < 15:
            return "MEDIUM"
        else:
            return "HIGH"

    def get_signal_time(self, density, emergency_flag):

        if emergency_flag:
            return 10

        if density == "LOW":
            return 15
        elif density == "MEDIUM":
            return 30
        else:
            return 60