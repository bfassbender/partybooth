# coding=UTF-8
import os

# Set this environment Variable to "true" in order to activate stubbing of the real gphoto2 interface
ENV_USE_CAMERA_STUB = "USE_CAMERA_STUB"

# Do not change from here
PWD = os.path.abspath(os.path.dirname(__file__))

TITLE_FONT = ("Roboto Condensed", 18, "bold")

CAPTURE_FOLDER = os.path.join("/media/usb")

TEMP_FOLDER = os.path.join("/media/usb/temp")

PHOTOS_FOLDER = os.path.join(PWD, "photos")

STUB_IMAGE_FOLDER = os.path.join(PWD, "tests/images")

FONT_FACE = "Roboto Condensed"
FONT_SIZE_HUGE = 200
FONT_SIZE_SEMI_HUGE = 150
FONT_SIZE_BIG = 80
FONT_SIZE_MEDIUM = 60
