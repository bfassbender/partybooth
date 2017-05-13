# coding=UTF-8
import Tkinter as tk

import constants as CONSTANTS


class ConnectionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=800, height=480)
        self.pack_propagate(0)

        self.controller = controller

        self.label = tk.Label(self, fg='white', bg='DarkOrange1', borderwidth=10,
                              text="Ich bereite alles vor.\nDie PartyBooth ist\ngleich startklar...",
                              font=(CONSTANTS.FONT_FACE, CONSTANTS.FONT_SIZE_MEDIUM))
        self.label.pack(fill=tk.BOTH, expand=True)
