# coding=UTF-8
import logging
import os
import time
import shutil
from datetime import datetime
import constants as CONSTANTS

from subprocess import check_output
import subprocess

CAPTURETARGET_INTERNAL_RAM = 0
CAPTURETARGET_MEMORY_CARD = 1

IMAGEFORMAT_JPG_LARGE_FINE = 0
IMAGEFORMAT_JPG_LARGE_NORMAL = 1
IMAGEFORMAT_JPG_MEDIUM_FINE = 2
IMAGEFORMAT_JPG_MEDIUM_NORMAL = 3
IMAGEFORMAT_JPG_SMALL_FINE = 4
IMAGEFORMAT_JPG_SMALL_NORMAL = 5

class CameraAdapter(object):
    IMAGE_EXTENSION = '.jpg'
    logger = logging.getLogger("PartyBooth.CameraAdapter")

    def __init__(self):
        try:
            self.logger.debug("Resetting USB")
            output = check_output(["gphoto2", "--reset", "-q"], stderr=subprocess.STDOUT)
            self.logger.debug(output)
        except subprocess.CalledProcessError as ex:
            self.logger.warn("Resetting USB failed with returncode {0} and output '{1}'".format(ex.returncode, ex.output))

        self.logger.info(check_output(["gphoto2", "--auto-detect"], stderr=subprocess.STDOUT))
        self.logger.info("CameraAdapter initialized!")

    def connectToCamera(self):
        self.logger.info("Connecting to Camera...")
        try:
            self._setCaptureTarget(CAPTURETARGET_INTERNAL_RAM)
            self._setCaptureFormat(IMAGEFORMAT_JPG_LARGE_FINE)
            self.logger.info("Connection successful!")

        except subprocess.CalledProcessError as gpe:
            self.logger.error("Connection to camera failed with returncode {0} and output {1}".format(gpe.returncode, gpe.output))
            raise gpe

    def takePicture(self, photoset):
        self.logger.info("Taking Photo...")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S');
        filename = "%s_%s_%s.jpg" % (timestamp, photoset['id'], len(photoset['photos']) + 1)
        tmp_path = os.path.join(CONSTANTS.TEMP_FOLDER, filename)
        target_path = os.path.join(CONSTANTS.CAPTURE_FOLDER, filename)

        start_time = time.time()
        try:
            output = check_output(['gphoto2', '--capture-image-and-download', '--keep', '--force-overwrite', '--filename', tmp_path], stderr=subprocess.STDOUT)
            self.logger.info("Taking Picture successful with output {0}".format(output))

        except subprocess.CalledProcessError as gpe:
            self.logger.error("Taking Picture failed with returncode {0} and output\n{1}".format(gpe.returncode, gpe.output))
            raise gpe

        elapsed_time = time.time() - start_time
        self.logger.debug('Capture and download took {0} seconds'.format(elapsed_time))

        if os.path.isfile(tmp_path):
            photoset['photos'].append(target_path)
            photoset['thumbs'].append(tmp_path)
            self.logger.info("Added Photo to Photoset " + tmp_path)
        else:
            raise Exception("File expected in path {0} but none found.".format(target_path))

    def _setCaptureTarget(self, target):
        self._setCameraParameter('capturetarget', target)

    def _setCaptureFormat(self, format):
        self._setCameraParameter('imageformat', format)
        self._setCameraParameter('imageformatcf', format)

    def _setCameraParameter(self, parameter, to_value):
        self.logger.info("Setting camera config parameter '{0}' to value '{1}'".format(parameter,to_value))
        param_string = parameter + "=" + str(to_value)
        self.logger.debug(check_output(["gphoto2","--set-config", param_string], stderr=subprocess.STDOUT))

class FakeCameraAdapter(CameraAdapter):
    logger = logging.getLogger("FakeCameraAdapter")

    def takePicture(self, photoset):
        self.logger.info('Enter: takePicture')
        camera_path = os.path.join(CONSTANTS.STUB_IMAGE_FOLDER,
                                   str(len(photoset['photos']) + 1) + self.IMAGE_EXTENSION)
        photoset['camerapaths'].append(camera_path)

    def connectToCamera(self):
        self.logger.info('Enter: connectToCamera')

    def transferPicture(self, photoset):
        self.logger.info('Enter: transferPicture')
        camera_path = photoset['camerapaths'][len(photoset['camerapaths']) - 1]
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S');
        filename = "%s_%s_%s.jpg" % (timestamp, photoset['id'], len(photoset['photos']) + 1)
        target_path = os.path.join(CONSTANTS.CAPTURE_FOLDER, filename)
        self.logger.info('Copying image from {0} to {1}'.format(camera_path, target_path))
        shutil.copy(camera_path, target_path)
        photoset['photos'].append(target_path)
        self.logger.info("Added Photo to Photoset " + target_path)
