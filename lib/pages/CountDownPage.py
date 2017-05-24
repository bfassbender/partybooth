# coding=UTF-8
import Tkinter as tk
import time

import constants as CONSTANTS


class CountDownPage(tk.Frame):
    COUNTDOWN_TICK_LENGTH = 1

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=800, height=480)
        self.pack_propagate(0)
        self.controller = controller

        self.countdownLength = 3

        self.countdownText = tk.StringVar()
        self.countdownText.set(self.countdownLength)
        self.countdownLabel = tk.Label(self, fg='white', bg='green', borderwidth=10,
                                       textvariable=self.countdownText,
                                       font=(CONSTANTS.FONT_FACE, CONSTANTS.FONT_SIZE_HUGE))

        self.smileLabel = tk.Label(self, fg='white', bg='green', borderwidth=10,
                                   text='SMILE :)',
                                   font=(CONSTANTS.FONT_FACE, CONSTANTS.FONT_SIZE_SEMI_HUGE))

    def countDown(self):
        self.showCountDownLabel()
        time.sleep(self.COUNTDOWN_TICK_LENGTH)

        counter = self.countdownLength
        for i in range(counter):
            self.countdownText.set(str(counter - i))
            self.countdownLabel.update()
            time.sleep(self.COUNTDOWN_TICK_LENGTH)

        self.showSmileLabel()

    def showSmileLabel(self):
        self.countdownLabel.forget()
        self.smileLabel.pack(fill=tk.BOTH, expand=True)
        self.update()
        #time.sleep(.3)

    def showCountDownLabel(self):
        self.smileLabel.forget()
        self.countdownLabel.pack(fill=tk.BOTH, expand=True)
        self.countdownText.set("Bereit?")
        self.update()
