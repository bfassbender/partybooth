# coding=UTF-8
import logging
import os
import shutil
from datetime import datetime
import gphoto2 as gp
import constants as CONSTANTS

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
        gp.check_result(gp.use_python_logging())
        self.context = gp.Context()
        self.camera = gp.Camera()

    def connectToCamera(self):
        try:
            self.logger.info("Connecting to Camera...")
            self._init_camera()
            self._setCaptureTarget(CAPTURETARGET_INTERNAL_RAM)
            self._setCaptureFormat(IMAGEFORMAT_JPG_LARGE_FINE)
            self.logger.info("Connection successful!")
        finally:
            self._exit_camera()

    def takePicture(self, photoset):
        try:
            self.logger.info("Taking Photo...")
            self._init_camera()
            # subprocess.call(['gphoto2', '--capture-image-and-download', '--keep', '--force-overwrite', '--filename', target_path])
            camera_path = self.camera.capture(gp.GP_CAPTURE_IMAGE, self.context)
            self.logger.info('Image on camera {0}/{1}'.format(camera_path.folder, camera_path.name))
            photoset['camerapaths'].append(camera_path)

        except Exception as e:
            self._exit_camera() # only exit on exception as we need to keep camera-connection or capturing to camera RAM will fail on camera.file_get().
            raise e

    def transferPicture(self, photoset):
        try:
            camera_path = photoset['camerapaths'][len(photoset['camerapaths']) - 1]
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S');
            filename = "%s_%s_%s.jpg" % (timestamp, photoset['id'], len(photoset['photos']) + 1)
            tmp_path = os.path.join(CONSTANTS.TEMP_FOLDER, filename)
            target_path = os.path.join(CONSTANTS.CAPTURE_FOLDER, filename)
            self.logger.debug('Retrieving image from {0}/{1} to {2}'.format(camera_path.folder, camera_path.name, tmp_path))
            # self._init_camera()
            camera_file = self.camera.file_get(camera_path.folder, camera_path.name, gp.GP_FILE_TYPE_NORMAL, self.context)
            camera_file.save(tmp_path)
            self.logger.debug(
            'Deleting image from {0}/{1} on camera.'.format(camera_path.folder, camera_path.name))
            self.camera.file_delete(camera_path.folder, camera_path.name, self.context)
        finally:
            self._exit_camera()

        if os.path.isfile(tmp_path):
            photoset['photos'].append(target_path)
            photoset['thumbs'].append(tmp_path)
            self.logger.info("Added Photo to Photoset " + target_path)
        else:
            raise Exception("File expected in path {0} but none found.".format(target_path))

    def _setCaptureTarget(self, target):
        self._setCameraParameter('capturetarget', target)

    def _setCaptureFormat(self, format):
        self._setCameraParameter('imageformat', format)
        self._setCameraParameter('imageformatcf', format)

    def _setCameraParameter(self, parameter, to_value):
        self.logger.info("Setting camera config parameter '{0}' to value '{1}'".format(parameter,to_value))
        # get configuration tree
        config = gp.check_result(gp.gp_camera_get_config(self.camera, self.context))
        # find the capture target config item
        capture_target = gp.check_result(gp.gp_widget_get_child_by_name(config, parameter))
        value = gp.check_result(gp.gp_widget_get_choice(capture_target, to_value))
        gp.check_result(gp.gp_widget_set_value(capture_target, value))
        # set config
        gp.check_result(gp.gp_camera_set_config(self.camera, config, self.context))

    def __delete__(self, instance):
        self.logger.debug("Destructor: Exiting Camera.")
        instance.camera.exit(instance.context)

    def _init_camera(self):
        self.logger.debug("Initializing Camera.")
        self.camera.init(self.context)

    def _exit_camera(self):
        self.logger.debug("Exiting Camera.")
        self.camera.exit(self.context)

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
