import cv2
import numpy as np
from PIL import Image
from constants import *

class Apriltag:
    def __init__(self):
        template_ul = cv2.imread(APRILTAG_IMAGE['ul'])
        template_dr = cv2.imread(APRILTAG_IMAGE['dr'])
        self.template_gray_ul = cv2.cvtColor(template_ul, cv2.COLOR_BGR2GRAY)
        self.template_gray_dr = cv2.cvtColor(template_dr, cv2.COLOR_BGR2GRAY)
    
    def MatchTemplate(self, image: Image.Image, return_image=False):
        image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        
        w_ul, h_ul = self.template_gray_ul.shape[::-1]
        w_dr, h_dr = self.template_gray_dr.shape[::-1]
        
        result_ul = cv2.matchTemplate(image_gray, self.template_gray_ul, cv2.TM_CCOEFF_NORMED)
        min_val_ul, max_val_ul, min_loc_ul, max_loc_ul = cv2.minMaxLoc(result_ul)
        top_left_ul = max_loc_ul
        bottom_right_ul = (top_left_ul[0] + w_ul, top_left_ul[1] + h_ul)
        
        result_dr = cv2.matchTemplate(image_gray, self.template_gray_dr, cv2.TM_CCOEFF_NORMED)
        min_val_dr, max_val_dr, min_loc_dr, max_loc_dr = cv2.minMaxLoc(result_dr)
        top_left_dr = max_loc_dr
        bottom_right_dr = (top_left_dr[0] + w_dr, top_left_dr[1] + h_dr)
        
        # 计算匹配区域的中心坐标
        xyxy = (
            (top_left_ul[0] + bottom_right_ul[0]) / 2, 
            (top_left_ul[1] + bottom_right_ul[1]) / 2, 
            (top_left_dr[0] + bottom_right_dr[0]) / 2, 
            (top_left_dr[1] + bottom_right_dr[1]) / 2
        )
        
        annotated_image = None
        if return_image:
            annotated_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.rectangle(annotated_image, top_left_ul, bottom_right_ul, (0, 255, 0), 2)
            cv2.rectangle(annotated_image, top_left_dr, bottom_right_dr, (0, 255, 0), 2)
            cv2.circle(annotated_image, (int(xyxy[0]), int(xyxy[1])), 5, (0, 0, 255), -1)
            cv2.circle(annotated_image, (int(xyxy[2]), int(xyxy[3])), 5, (0, 0, 255), -1)
        
        return annotated_image, xyxy
            
        
if __name__ == "__main__":
    img_file_path = "image/test7.PNG"
    img = Image.open(img_file_path)
    apriltag = Apriltag()
    annotated_image, xyxy = apriltag.MatchTemplate(img, return_image=True)
    cv2.imshow('AprilTag', annotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(xyxy)
