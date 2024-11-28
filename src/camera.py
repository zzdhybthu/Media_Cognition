import cv2
from constants import *
from PIL import Image

class Camera():
    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_IDX)
        if not self.cap.isOpened():
            raise Exception("Cannot open camera")
    
    def Capture(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Cannot receive frame (camera disconnected).")
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    def Release(self):
        self.cap.release()
        cv2.destroyAllWindows()