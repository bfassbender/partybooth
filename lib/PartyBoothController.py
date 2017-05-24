# coding=UTF-8
import logging
import os
import uuid
import RPi.GPIO as GPIO
import atexit
import shutil

import gphoto2 as gp

import constants as CONSTANTS
from lib.CameraAdapter import FakeCameraAdapter, CameraAdapter
from lib.pages.CountDownPage import CountDownPage
from lib.pages.ErrorPage import ErrorPage
from lib.pages.PhotoReviewPage import PhotoReviewPage
from lib.pages.StartPage import StartPage
from lib.pages.ConnectionPage import ConnectionPage

class PartyBoothController(object):
    logger = logging.getLogger("PartyBooth.PartyBoothController")

    STATE_INITIALIZING = "initializing"
    STATE_READY = "ready"
    STATE_CAPTURING = "capturing"
    STATE_REVIEWING = "reviewing"
    STATE_ERROR = "error"

    def __init__(self, partyBoothUI):
        self.partyBoothUI = partyBoothUI
        self.cameraAdapter = self.createCameraAdapter()
        self.setupGpio()
        self.current_state = None
        self.setCurrentStateTo(PartyBoothController.STATE_INITIALIZING)
        self.logger.info("Controller initialized.")
        self.logger.info("GPIO Version is %s" % GPIO.VERSION)

    def startCountDown(self):
        page = self.partyBoothUI.showPage(CountDownPage.__name__)
        page.showSmileLabel()
        photoset = self.createPhotoset()
        self.capturePhoto(photoset)

    @staticmethod
    def createPhotoset():
        guid = uuid.uuid4().hex[:16]
        return {'id': guid, 'photos': [], 'thumbs': [], 'camerapaths': []}

    def capturePhoto(self, photoset):
        self.setCurrentStateTo(PartyBoothController.STATE_CAPTURING)
        try:
            #for i in range(1,200):
            self.cameraAdapter.takePicture(photoset)
            frame = self.partyBoothUI.showPage(PhotoReviewPage.__name__)
            self.cameraAdapter.transferPicture(photoset)
            self.setCurrentStateTo(PartyBoothController.STATE_REVIEWING)
            frame.displayLastPhoto(photoset)
        except Exception as e:
            self.logger.error("Taking Picture failed")
            self.setCurrentStateTo(PartyBoothController.STATE_ERROR)
            self.logger.exception(e)
            self.partyBoothUI.showPage(ErrorPage.__name__)

    def prepare_directory_structure(self):
        self.create_folder(CONSTANTS.CAPTURE_FOLDER)
        self.create_folder(CONSTANTS.TEMP_FOLDER)
        self.create_folder(CONSTANTS.PHOTOS_FOLDER)

    def create_folder(self, path):
        try:
            os.makedirs(path)
            self.logger.info("Created folder " + path)
        except OSError:
            if not os.path.isdir(path):
                raise

    def saveToStick(self, photoset):
        src_path = photoset['thumbs'][len(photoset['thumbs']) - 1]
        target_path = photoset['photos'][len(photoset['photos']) - 1]
        self.logger.debug('Moving image from {0} to {1}'.format(src_path, target_path))
        shutil.copyfile(src_path, target_path)
        os.remove(src_path)

    def createCameraAdapter(self):
        useFake = os.environ.get(CONSTANTS.ENV_USE_CAMERA_STUB)

        if useFake:
            self.logger.warn("USE_CAMERA_STUB IS ACTIVE!")
            return FakeCameraAdapter()
        else:
            self.logger.info("USING REAL CAMERA ADAPTER")
            return CameraAdapter()

    def setCameraAdapter(self, adapter):
        assert isinstance(adapter, CameraAdapter)
        self.cameraAdapter = adapter

    def showPage(self, page):
        return self.partyBoothUI.showPage(page)

    def getReadyForNextCapture(self):
        self.showPage(StartPage.__name__)
        self.setCurrentStateTo(PartyBoothController.STATE_READY)

    def connectToCamera(self):
        frame = self.showPage(ConnectionPage.__name__)
        self.checkCameraConnection(frame)

    def resetBooth(self):
        self.cameraAdapter = self.createCameraAdapter()
        self.connectToCamera()

    def checkCameraConnection(self, frame):
        self.logger.info("Checking camera connection...")

        try:
            self.cameraAdapter.connectToCamera()
            self.getReadyForNextCapture()
        except gp.GPhoto2Error as ex:
            if ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                self.logger.warn("Could not connect to camera. Retrying ...")
                frame.after(2000, self.checkCameraConnection, frame)
            else:
                self.setCurrentStateTo(PartyBoothController.STATE_ERROR)
                self.logger.exception(ex)
                self.partyBoothUI.showPage(ErrorPage.__name__)

    def onRfButtonPressed(self, event):
        if PartyBoothController.STATE_READY == self.current_state:
            self.startCountDown()
        else:
            self.logger.info("Ignoring Button press. Current state [%s] does not match [%s]" % (self.current_state, PartyBoothController.STATE_READY))

    
    def setupGpio(self):
        self.logger.info("Setting up GPIO...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(CONSTANTS.GPIO_PIN_17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(CONSTANTS.GPIO_PIN_17, GPIO.RISING, callback=self.onRfButtonPressed, bouncetime=200)
        self.logger.info("GPIO ready!")

    def setCurrentStateTo(self, state):
        self.current_state = state
        self.logger.info("STATE is [%s]" % self.current_state)


@atexit.register
def onExit():
    logging.getLogger("PartyBooth.PartyBoothController").info("Cleanig up GPIO...")
    GPIO.cleanup()

