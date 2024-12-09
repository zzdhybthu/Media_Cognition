
import threading
import keyboard
from matplotlib import pyplot as plt

from camera import Camera
from arm import Arm
from audio import Audio
from match import Match
from proposal import Proposal
from constants import *



class TOP():
    def __init__(self):
        print("==================== Initializing ====================")
        print("Initializing Camera ...")
        self.camera = Camera()
        print("Initializing Arm ...")
        self.arm = Arm()
        print("Initializing Audio ...")
        self.audio = Audio()
        print("Initializing Match ...")
        self.match = Match()
        print("Initializing Proposal ...")
        self.proposal = Proposal()
        print("All Initializations Completed\n")
    
    def SplitPrompt():
        prompt = ""
        with open(r'prompt.txt','r',encoding='utf-8') as test:
            test.seek(0, 0)
            prompt = test.readline()   
        prompt = prompt.split(' ')
        obj = prompt[1]
        box = prompt[3]
        # print(type((obj, box)))
        return (obj, box)
    
    def Process(self):
        print("==================== Process ====================")
        print("Init Arm ...")
        self.arm.INIT()
        
        print("Listen and Recognize ...")
        self.audio.listen_and_recognize()
        prompt = self.SplitPrompt()
        if prompt is None:
            raise ValueError("Failed to recognize audio")
        from_object, to_object = self.SplitPrompt(prompt)
        print(f"{from_object=} -> {to_object=}")
        
        print("Capture Image ...")
        image = self.camera.Capture()
        
        print("Propose Regions ...")
        annotations = self.proposal.Propose(image)
        print(f"{annotations=}")
        cropped_images = []
        for annotation in annotations:
            xyxy = annotation["box"]
            cropped_image = image.crop(xyxy)  # TODO: should be verified
            cropped_images.append(cropped_image)
        
        print("Match for object ...")
        _, max_index = self.match.Img2Txt(cropped_images, from_object)
        from_target = annotations[max_index]
        from_x = (from_target["box"][0] + from_target["box"][2]) / 2
        from_y = (from_target["box"][1] + from_target["box"][3]) / 2
        print(f"{from_x=}, {from_y=}")
        
        print("Match for bins ...")
        _, max_index = self.match.Img2Txt(BIN_IMAGE, to_object)
        tag = COORDS[BIN_POS[max_index]]
        print(f"{BIN_IMAGE[max_index]=}, {tag=}")
        
        print("Get ...")
        self.arm.GET(from_x, from_y)
        
        print("Put ...")
        self.arm.PUT(tag)
        
        

if __name__ == '__main__':

    # top = TOP()
    # while True:
    #     print("Press Enter to start ...")
    #     keyboard.wait("enter")
    #     threading.Thread(target=top.Process).start()
    #     print("Press Enter to restart / Press Esc to exit ...")
    #     if keyboard.wait("esc"):
    #         break
    # print("Exiting ...")
    # top.camera.Release()
    # print("Exited")

    myCamera = Camera()
    img = myCamera.Capture()
    # img.save("camera_image.jpg")
    # img.show()
    myCamera.Release()


    # image_path = './image/test4.jpg'
    # with Image.open(image_path) as img:
    # 此处硬切割，必须保证相机位置不变！！！
    cropped_img = img.crop((220, 140, 450, 380)) # 230*240
    cropped_img.show()
    # cropped_img.save('cropped_image.jpg')

    proposal = Proposal()
    w, h = cropped_img.size
    annotated_image, annotations = proposal.Propose(cropped_img, return_image=True)
    print(annotations)
    cv2.imshow("Annotated Image", annotated_image)
    cv2.waitKey(0)

    arm = Arm('COM17')
    arm.INIT()

    for i in range(len(annotations)):
        coords = annotations[i]["box"]

        x_norm = (coords[0] + coords[2]) / (2*230)
        y_norm = (coords[1] + coords[3]) / (2*240)

        arm.GET(pixel_x = x_norm, pixel_y = y_norm)
        arm.PUT('ur')
