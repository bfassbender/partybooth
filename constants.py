# coding=UTF-8
import os

# Set this environment Variable to "true" in order to activate stubbing of the real gphoto2 interface
ENV_USE_CAMERA_STUB = "USE_CAMERA_STUB"

# Do not change from here
PWD = os.path.abspath(os.path.dirname(__file__))

GPIO_PIN_17 = 17

CAPTURE_FOLDER = os.path.join("/media/usb")

TEMP_FOLDER = os.path.join("/tmp")

PHOTOS_FOLDER = os.path.join(PWD, "photos")

STUB_IMAGE_FOLDER = os.path.join(PWD, "tests/images")

FONT_FACE = "FreeSans"
FONT_SIZE_HUGE = 200
FONT_SIZE_SEMI_HUGE = 135
FONT_SIZE_LARGE = 80
FONT_SIZE_MEDIUM = 60
