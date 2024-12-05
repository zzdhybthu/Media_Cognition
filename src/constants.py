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
TRANSIT_COORD = [178.0, -14.4, 263.0, 177.55, -0.31, -116.12]

FORWARD_TIME = 9

PUMP_PORT = [2, 5]
PUMP_Z_1 = 135  # before
PUMP_Z_2 = 90  # during
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
        [[219.3, 145.4, 234.3, -164.05, 18.16, -82.93],  # up
         [219.3, 145.4, 234.3, -164.05, 18.16, -82.93]],  # down
    "ur": # right-far
        [[212.8, -137.2, 246.3, -160.06, 12.55, -129.97],  # up
         [212.8, -137.2, 246.3, -160.06, 12.55, -129.97]],  # down
    "bl": # left-near
        [[121.9, 162.7, 252.4, 179.95, 1.68, -58.87],  # up
         [121.9, 162.7, 252.4, 179.95, 1.68, -58.87]],  # down
    "br": # right-near
        [[130.8, -150.3, 254.8, 179.63, 3.7, -145.87],  # up
         [130.8, -150.3, 254.8, 179.63, 3.7, -145.87]],  # down
}


"""
utils
"""
BORDER_LEFT = 80
BORDER_RIGHT = -64
BORDER_BOTTOM = 107.4
BORDER_TOP = 231.5

ARUCO_BOTTOM_RIGHT = [0.10281276, 0.08772572]
ARUCO_UPPER_LEFT = [0.10281276 - 0.15, 0.08772572 - 0.15]

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