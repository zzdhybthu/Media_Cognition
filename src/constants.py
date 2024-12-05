"""
status, not used
"""

SUCCESS = 0
FAILURE = 1
EXCEPTION = 2


"""
arm
"""

COORD_MODE = 0  # 0 - angluar, 1 - linear
DELTA = 15

DEFAULT_SPEED = 80
DEFAULT_COORD = [50, -60, 400, -90, 0, -90]

FORWARD_TIME = 9

PUMP_PORT = [2, 5]
PUMP_Z_1 = 135  # before
PUMP_Z_2 = 105  # during
PUMP_Z_3 = 155  # after
PUMP_ANGLE = [180, 0, 180]
PUMP_SPEED = 20
PUMP_TIME_1 = 0  # pump on
PUMP_TIME_2 = 4  # pump off
COORDS = {
    "c": # center
        [[150, 0, 240, -180, 0, 0],  # up
         [150, 0, 175, -180, 0, 0]],  # down
    "ul": # left-far
        [[200, 110, 240, -180, 0, 0],  # up
         [215, 150, 220, -150, 0, -60]],  # down
    "ur": # right-far
        [[200, -100, 240, -180, 0, 0],  # up
         [220, -140, 220, -150, -10, -80]],  # down
    "bl": # left-near
        [[120, 170, 240, -180, 0, 0],  # up
         [120, 170, 175, -180, 0, 0]],  # down
    "br": # right-near
        [[120, -150, 240, -180, 0, 0],  # up
         [120, -150, 175, -180, 0, 0]],  # down
}


"""
utils
"""
BORDER_LEFT = 80
BORDER_RIGHT = -70
BORDER_BOTTOM = 90
BORDER_TOP = 235


"""
audio
"""
RECORD_TIME = 5
MODE = "whisper"  # "sphinx" or "google" or "whisper"


"""
proposal
"""
MODEL_ID = "yolov10m"
IMAGE_SIZE = 640
THRERSHOLD = 0.5


"""
match
"""
MODEL_NAME = "ViT-B/32"


"""
camera
"""
CAMERA_IDX = 0


"""
main
"""
BIN_IMAGE = [
    "./image/blue.jpg",
    "./image/gray.jpg",
    "./image/green.jpg",
    "./image/red.jpg"
]
BIN_POS = ["ul", "ur", "bl", "br"]