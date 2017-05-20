#! /usr/bin/python

# import tkinter as tk   # python3
import Tkinter as tk  # python
import logging
import tkFont

from PIL import ImageTk

import constants as CONSTANTS
from lib.PartyBoothController import PartyBoothController
from lib.pages.ConnectionPage import ConnectionPage
from lib.pages.CountDownPage import CountDownPage
from lib.pages.ErrorPage import ErrorPage
from lib.pages.PhotoReviewPage import PhotoReviewPage
from lib.pages.StartPage import StartPage


class PartyBooth(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.configureLogging()
        self.logger = logging.getLogger("PartyBooth")

        self.logger.info("####################################################################")
        self.logger.info("#                      PARTYBOOTH STARTING UP                      #")
        self.logger.info("####################################################################")

        # self.geometry("800x480")
        self.attributes("-fullscreen", True)

        self.frames = {}
        self.current_frame = None
        self.controller = PartyBoothController(self)
        self.controller.prepare_directory_structure()

        self.paintBackground()

        self.container = self.initializePageContainer()
        self.registerPages()
        # self.logFonts()
        self.logger.info("####################################################################")
        self.logger.info("#                        PARTYBOOTH STARTED                        #")
        self.logger.info("####################################################################")
        self.controller.connectToCamera()
        # background.lower()

    def logFonts(self):
        fonts = list(tkFont.families())
        fonts.sort()
        for font in fonts:
            self.logger.debug(font)

    def showPage(self, page_name):
        self.logger.info("Showing '%s'" % page_name)
        # Show a frame for the given page name
        # only raise frame in question leaving the rest untouched
        # frame = self.frames[page_name]
        # frame.tkraise()

        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()
        self.update()
        frame.event_generate("<<PAGE_ACTIVATED>>")
        self.current_frame = frame
        return frame

    def initializePageContainer(self):
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others, or grid.remove()d
        container = tk.Frame(self)
        # container.pack(side="top", fill="both", expand=True)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # container.grid_propagate(0)
        return container

    def registerPages(self):
        for F in (StartPage, CountDownPage, PhotoReviewPage, ConnectionPage, ErrorPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self.controller)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

    def paintBackground(self):
        image = ImageTk.PhotoImage(file=CONSTANTS.PWD + '/resources/images/splash.png')
        background = tk.Label(self, image=image)
        background.image = image
        background.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    @staticmethod
    def configureLogging():
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        fh = logging.FileHandler('partybooth.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)

        # Configure Root Logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(ch)
        logger.addHandler(fh)

        # Configure Partybooth s Loggers
        logging.getLogger('PartyBooth').setLevel(logging.DEBUG)

        # Configure other Loggers
        logging.getLogger('gphoto2').setLevel(logging.ERROR)

    def getCurrentFrame(self):
        return self.current_frame

if __name__ == "__main__":
    app = PartyBooth()
    app.mainloop()
