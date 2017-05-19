# coding=UTF-8
import Tkinter as tk
import logging
import os
import subprocess

from PIL import ImageTk, Image

import constants as CONSTANTS


class PhotoReviewPage(tk.Frame):
    logger = logging.getLogger("PartyBooth.PhotoReviewPage")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=800, height=480)
        self.pack_propagate(0)
        self.controller = controller

        self.imageLabel = tk.Label(self, padx=0, pady=0, background='black')
        self.imageLabel.bind("<Button-1>", lambda event: self.returnToStartPage())

        self.label = tk.Label(self, fg='white', bg='DarkOrange1',
                              text="Ich verarbeite\ndas Foto...", font=(CONSTANTS.FONT_FACE, CONSTANTS.FONT_SIZE_LARGE))
        self.label.pack(fill=tk.BOTH, expand=True)

    # TODO has to be refactored intro controller
    def displayLastPhoto(self, photoset):

        photo_path = photoset['photos'][len(photoset['thumbs']) - 1]

        self.logger.info("Loading photo " + photo_path)
        load = Image.open(photo_path)
        self.logger.info("Photo loaded, format: (%s - %s - %s)" % (load.format, load.size, load.mode))

        self.logger.info("Resizing photo for display");
        baseHeight = 480
        heightRatio = (baseHeight / float(load.size[1]))
        calculatedWidth = int((float(load.size[0]) * float(heightRatio)))
        load = load.resize((calculatedWidth, baseHeight), Image.NEAREST)
        self.logger.info("Displaying photo")

        render = ImageTk.PhotoImage(image=load)

        self.imageLabel.image = render
        self.imageLabel.configure(image=render)

        self.label.pack_forget()
        self.imageLabel.pack(fill=tk.BOTH, expand=True)

        self.after_id = self.after(4000, self.returnToStartPage)
        self.logger.debug("Registered after_id: %s" % self.after_id)

    def returnToStartPage(self):
        self.logger.debug("Cancelled after_id: %s" % self.after_id)
        self.after_cancel(self.after_id)
        self.imageLabel.pack_forget()
        self.label.pack(fill=tk.BOTH, expand=True)
        self.controller.getReadyForNextCapture()
