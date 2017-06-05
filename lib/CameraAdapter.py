# coding=UTF-8
import logging
import os
import shutil
import time
from datetime import datetime
import gphoto2 as gp
import constants as CONSTANTS
from subprocess import check_output
from subprocess import CalledProcessError
import subprocess

CAPTURETARGET_INTERNAL_RAM = 0
CAPTURETARGET_MEMORY_CARD = 1

IMAGEFORMAT_JPG_LARGE_FINE = 0
IMAGEFORMAT_JPG_LARGE_NORMAL = 1
IMAGEFORMAT_JPG_MEDIUM_FINE = 2
IMAGEFORMAT_JPG_MEDIUM_NORMAL = 3
IMAGEFORMAT_JPG_SMALL_FINE = 4
IMAGEFORMAT_JPG_SMALL_NORMAL = 5

OFF=0
ON=1

class CameraAdapter(object):
    IMAGE_EXTENSION = '.jpg'
    logger = logging.getLogger("PartyBooth.CameraAdapter")

    def __init__(self):
        try:
            self.logger.debug("Resetting USB " + check_output(["gphoto2", "--reset", "-q"], stderr=subprocess.STDOUT))
        except CalledProcessError as ex:
            self.logger.warn("Resetting USB failed with Retcode {0} and message '{1}'".format(ex.returncode, ex.output))

        gp.check_result(gp.use_python_logging())

    def connectToCamera(self):
        self.logger.info("Connecting to Camera...")
        self._setCaptureTarget(CAPTURETARGET_INTERNAL_RAM)
        self._setCaptureFormat(IMAGEFORMAT_JPG_LARGE_FINE)
        self._setAutoPoweroff(OFF)
        self.logger.info("Connection successful!")

    def takePicture(self, photoset):
        self.logger.info("Taking Photo...")
        start_time = time.time()
        context = gp.gp_context_new()
        camera = None
        try:
            camera = gp.check_result(gp.gp_camera_new())
            gp.check_result(gp.gp_camera_init(camera, context))
            camera_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE, context))
            self.logger.info('Image on camera {0}/{1}'.format(camera_path.folder, camera_path.name))
            photoset['camerapaths'].append(camera_path)

            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S');
            filename = "%s_%s_%s.jpg" % (timestamp, photoset['id'], len(photoset['photos']) + 1)
            tmp_path = os.path.join(CONSTANTS.TEMP_FOLDER, filename)
            target_path = os.path.join(CONSTANTS.CAPTURE_FOLDER, filename)

            self.logger.debug('Retrieving image from {0}/{1} to {2}'.format(camera_path.folder, camera_path.name, tmp_path))
            camera_file = gp.check_result(gp.gp_camera_file_get(camera, camera_path.folder, camera_path.name, gp.GP_FILE_TYPE_NORMAL, context))
            gp.check_result(gp.gp_file_save(camera_file, tmp_path))

            if os.path.isfile(tmp_path):
                photoset['photos'].append(target_path)
                photoset['thumbs'].append(tmp_path)
                self.logger.info("Added Photo to Photoset " + tmp_path)
            else:
                raise Exception("File expected in path {0} but none found.".format(target_path))

        finally:
            if camera and context:
                self.logger.debug("Exiting Camera")
                gp.check_result(gp.gp_camera_exit(camera, context))
                elapsed_time = time.time() - start_time
                self.logger.info('Capture and download took {0} seconds'.format(elapsed_time))

    def _setCaptureTarget(self, target):
        self._setCameraParameter('capturetarget', target)

    def _setCaptureFormat(self, format):
        self._setCameraParameter('imageformat', format)
        self._setCameraParameter('imageformatcf', format)

    def _setAutoPoweroff(self, value):
        #self._setCameraParameter('autopoweroff', value)
        pass

    def _setCameraParameter(self, parameter, to_value):
        context = gp.gp_context_new()
        camera = None
        try:
            camera = gp.check_result(gp.gp_camera_new())
            gp.check_result(gp.gp_camera_init(camera, context))

            self.logger.info("Setting camera config parameter '{0}' to value '{1}'".format(parameter, to_value))
            # get configuration tree
            config = gp.check_result(gp.gp_camera_get_config(camera, context))
            # find the capture target config item
            capture_target = gp.check_result(gp.gp_widget_get_child_by_name(config, parameter))
            value = gp.check_result(gp.gp_widget_get_choice(capture_target, to_value))
            gp.check_result(gp.gp_widget_set_value(capture_target, value))
            # set config
            gp.check_result(gp.gp_camera_set_config(camera, config, context))
        finally:
            if camera and context:
                self.logger.debug("Exiting Camera")
                gp.check_result(gp.gp_camera_exit(camera, context))

class FakeCameraAdapter(CameraAdapter):
    logger = logging.getLogger("FakeCameraAdapter")

    def takePicture(self, photoset):
        self.logger.info('Enter: takePicture')
        camera_path = os.path.join(CONSTANTS.STUB_IMAGE_FOLDER,
                                   str(len(photoset['photos']) + 1) + self.IMAGE_EXTENSION)
        photoset['camerapaths'].append(camera_path)
        camera_path = photoset['camerapaths'][len(photoset['camerapaths']) - 1]
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S');
        filename = "%s_%s_%s.jpg" % (timestamp, photoset['id'], len(photoset['photos']) + 1)
        target_path = os.path.join(CONSTANTS.CAPTURE_FOLDER, filename)
        self.logger.info('Copying image from {0} to {1}'.format(camera_path, target_path))
        shutil.copy(camera_path, target_path)
        photoset['photos'].append(target_path)
        self.logger.info("Added Photo to Photoset " + target_path)

    def connectToCamera(self):
        self.logger.info('Enter: connectToCamera')

