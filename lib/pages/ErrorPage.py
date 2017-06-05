# coding=UTF-8
import Tkinter as tk

import logging

import constants as CONSTANTS


class ErrorPage(tk.Frame):
    logger = logging.getLogger("PartyBooth.ErrorPage")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=800, height=480)
        self.pack_propagate(0)

        self.controller = controller

        self.label = tk.Label(self, fg='white', bg='red', borderwidth=10,
                              text="Oops!\nEs gab leider ein\nProblem. Probieren \nwir es nochmal...",
                              font=(CONSTANTS.FONT_FACE, CONSTANTS.FONT_SIZE_MEDIUM))
        self.label.pack(fill=tk.BOTH, expand=1)
        self.label.bind("<Button-1>", lambda event: self.callBoothReset())
        self.bind("<<PAGE_ACTIVATED>>", lambda event: self.startReturnToStartPageTimer())

    def callBoothReset(self):
        self.logger.debug("Cancelled after_id: %s" % self.after_id)
        self.after_cancel(self.after_id)
        self.controller.resetBooth()

    def startReturnToStartPageTimer(self):
        self.after_id = self.after(3000, self.callBoothReset)
        self.logger.debug("Registered after_id: %s" % self.after_id)
