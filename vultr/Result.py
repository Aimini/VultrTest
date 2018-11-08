# -*- coding: utf-8 -*-
# time: 2018-11-06 19:46:13
# Author: AI

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

    def setCSPackage(self, sent, received, loss, loss_rate):
        self.CS_sent = sent
        self.CS_received = received
        self.CS_loss = loss
        self.CS_loss_rate = loss_rate


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

    def setSCPackage(self,sent,received,loss,loss_rate):
        self.SC_sent = sent
        self.SC_received = received
        self.SC_loss = loss
        self.SC_loss_rate = loss_rate


    def setSpeed(self, speed_max, speed_avg):
        """
        set download speed in client
        :param speed_avg
        """
        self.speed_max = speed_max
        self.speed_avg = speed_avg

    def __repr__(self):
        return str(vars(self))
