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
    

myCamera = Camera()
img = myCamera.Capture()
# img.save("camera_image.jpg")
# img.show()
myCamera.Release()


# image_path = './image/test4.jpg'
# with Image.open(image_path) as img:
# 此处硬切割，必须保证相机位置不变！！！
cropped_img = img.crop((220, 140, 450, 380))
cropped_img.show()
# cropped_img.save('cropped_image.jpg')