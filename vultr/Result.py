class Result:
    def setCSDelay(self, delay_min, delay_max, delay_avg):
        """
        set Client to Server Delay
        :param delay_min:
        :param delay_max:
        :param delay_avg:
        """
        self.CS_delay_min = delay_min
        self.CS_delay_max = delay_max
        self.CS_delay_avg = delay_avg

    def setSCDelay(self, delay_min, delay_max, delay_avg):
        """
        set Server to Client Delay
        :param delay_min:
        :param delay_max:
        :param delay_avg:
        """
        self.SC_delay_min = delay_min
        self.SC_delay_max = delay_max
        self.SC_delay_avg = delay_avg

    def setSpeed(self, speed_max, speed_avg):
        """
        set download speed in client
        :param speed_avg
        """
        self.speed_max = speed_max
        self.speed_avg = speed_avg
