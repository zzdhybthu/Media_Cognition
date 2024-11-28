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
    
    def SplitPrompt(self, prompt: str):
        assert 'put' and 'into' in prompt.lower()
        return prompt.split('put')[1].split('into')[0].strip(), prompt.split('into')[1].strip()
    
    def Process(self):
        print("==================== Process ====================")
        print("Init Arm ...")
        self.arm.INIT()
        
        print("Listen and Recognize ...")
        self.audio.Listen()
        self.audio.Recognize()
        prompt = self.audio.Prompt
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
    top = TOP()
    while True:
        print("Press Enter to start ...")
        keyboard.wait("enter")
        threading.Thread(target=top.Process).start()
        print("Press Enter to restart / Press Esc to exit ...")
        if keyboard.wait("esc"):
            break
    print("Exiting ...")
    top.camera.Release()
    print("Exited")
