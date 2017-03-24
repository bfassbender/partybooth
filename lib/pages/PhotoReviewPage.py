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
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.imageLabel = tk.Label(self, padx=0, pady=0, borderwidth=5, background='white')
        self.imageLabel.bind("<Button-1>", lambda event: self.returnToStartPage())

        self.label = tk.Label(self, fg='white', bg='red', borderwidth=10,
                              text="Verarbeite Foto...", font=(CONSTANTS.FONT_FACE, CONSTANTS.FONT_SIZE_BIG))
        self.label.pack(fill=tk.BOTH, expand=True)

    # TODO has to be refactored intro controller
    def displayLastPhoto(self, photoset):

        photo_path = photoset['photos'][len(photoset['thumbs']) - 1]

        thumb_filename = "thumb.jpg"
        thumb_path = os.path.join(CONSTANTS.TEMP_FOLDER, thumb_filename)

        self.logger.info("Creating Thumbnail " + thumb_path)
        subprocess.check_call(
            ['convert', photo_path, '-define', 'jpeg:size=1400x920', '-strip', '-thumbnail', '800x470', '-quality',
             '80', thumb_path])
        if os.path.isfile(thumb_path):
            photoset['thumbs'].append(thumb_path)
            self.logger.info("Added Thumbnail to Photoset " + thumb_path)
        else:
            self.logger.error("Error while creating thumbnail: " + thumb_path)

        self.logger.info("Loading Thumbnail " + thumb_path)
        load = Image.open(thumb_path)
        self.logger.info("Thumbnail Format: (%s - %s - %s)" % (load.format, load.size, load.mode))

        render = ImageTk.PhotoImage(image=load)

        self.imageLabel.image = render
        self.imageLabel.configure(image=render)

        self.label.pack_forget()
        self.imageLabel.pack()

        self.after_id = self.after(5000, self.returnToStartPage)
        self.logger.debug("Registered after_id: %s" % self.after_id)

    def returnToStartPage(self):
        self.logger.debug("Cancelled after_id: %s" % self.after_id)
        self.after_cancel(self.after_id)

        self.imageLabel.pack_forget()

        self.label.pack()
        self.controller.showPage('StartPage')
