
import threading
import keyboard
import cv2
from PIL import Image
from matplotlib import pyplot as plt

from camera import Camera
from arm import Arm
from audio import listen_and_recognize, zhipu_ai
from match import Match
from proposal import Proposal
from constants import *
from apriltag import Apriltag



# class TOP():
#     def __init__(self):
#         print("==================== Initializing ====================")
#         print("Initializing Camera ...")
#         self.camera = Camera()
#         print("Initializing Arm ...")
#         self.arm = Arm()
#         print("Initializing Audio ...")
#         self.audio = Audio()
#         print("Initializing Match ...")
#         self.match = Match()
#         print("Initializing Proposal ...")
#         self.proposal = Proposal()
#         print("All Initializations Completed\n")
    

    
    # def Process(self):
    #     print("==================== Process ====================")
    #     print("Init Arm ...")
    #     self.arm.INIT()
        
    #     print("Listen and Recognize ...")
    #     self.audio.listen_and_recognize()
    #     prompt = self.SplitPrompt()
    #     if prompt is None:
    #         raise ValueError("Failed to recognize audio")
    #     from_object, to_object = self.SplitPrompt(prompt)
    #     print(f"{from_object=} -> {to_object=}")
        
    #     print("Capture Image ...")
    #     image = self.camera.Capture()
        
    #     print("Propose Regions ...")
    #     annotations = self.proposal.Propose(image)
    #     print(f"{annotations=}")
    #     cropped_images = []
    #     for annotation in annotations:
    #         xyxy = annotation["box"]
    #         cropped_image = image.crop(xyxy)  # TODO: should be verified
    #         cropped_images.append(cropped_image)
        
    #     print("Match for object ...")
    #     _, max_index = self.match.Img2Txt(cropped_images, from_object)
    #     from_target = annotations[max_index]
    #     from_x = (from_target["box"][0] + from_target["box"][2]) / 2
    #     from_y = (from_target["box"][1] + from_target["box"][3]) / 2
    #     print(f"{from_x=}, {from_y=}")
        
    #     print("Match for bins ...")
    #     _, max_index = self.match.Img2Txt(BIN_IMAGE, to_object)
    #     tag = COORDS[BIN_POS[max_index]]
    #     print(f"{BIN_IMAGE[max_index]=}, {tag=}")
        
    #     print("Get ...")
    #     self.arm.GET(from_x, from_y)
        
    #     print("Put ...")
    #     self.arm.PUT(tag)
        
        

if __name__ == '__main__':

    # top = TOP()

    arm = Arm('COM17')
    arm.INIT()
    print("Arm Ready")

    myCamera = Camera()
    print("Camera Ready!")

    while True:
        print("Press Enter to start ...")
        keyboard.wait("enter")
        arm.INIT()
        
        img = myCamera.Capture()
        # img.save("camera_image.jpg")
        # img.show()

        # image_path = './image/test4.jpg'
        # with Image.open(image_path) as img:
        # 此处硬切割，必须保证相机位置不变！！！
        cropped_img = img.crop((200, 120, 460, 400)) # 260*280
        cropped_img.show()
        # cropped_img.save('cropped_image.jpg')

        apriltag = Apriltag()
        april_image, april_xyxy = apriltag.MatchTemplate(cropped_img, return_image=True)
        print(april_xyxy)

        proposal = Proposal()
        w, h = cropped_img.size
        annotated_image, annotations = proposal.Propose(cropped_img, return_image=True)
        print(annotations)
        cv2.imshow("Annotated Image", annotated_image)
        cv2.waitKey(0)


        listen_and_recognize()
        with open(r'prompt.txt','r',encoding='utf-8') as test:
            test.seek(0, 0)
            prompt = test.readline()
        
        match = Match()
        max_prob, max_box_index = match.Txt2Img(prompt, list(map(Image.open, ["image/gray.jpg", "image/green.jpg", "image/blue.jpg", "image/red.jpg"])))
        box_tag = BOX_INDEX[max_box_index]
        print(box_tag)

        img_list = []
        for i in range(len(annotations)):
            coords = annotations[i]["box"]
            img_i = cropped_img.crop((coords[0], coords[1], coords[2], coords[3]))
            # img_i.show()
            img_list.append(img_i)

        max_prob, max_obj_index = match.Txt2Img(prompt, img_list)
        coords = annotations[max_obj_index]["box"]
        print(max_obj_index)

        x_norm = (coords[0] + coords[2] - 2*april_xyxy[0]) / (2*(april_xyxy[2] - april_xyxy[0]))
        y_norm = (coords[1] + coords[3] - 2*april_xyxy[1]) / (2*(april_xyxy[3] - april_xyxy[1]))

        arm.GET(pixel_x = x_norm, pixel_y = y_norm)
        arm.PUT(box_tag)

        print("Press Enter to restart / Press Q to exit ...")
        keyboard_input = input()
        if keyboard_input == "q":
            break
    print("Exiting ...")
    myCamera.Release()
    print("Exited")

