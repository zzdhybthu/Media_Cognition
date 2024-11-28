from ultralytics import YOLOv10
from constants import *
import cv2
from PIL import Image


class Proposal():
    def __init__(self):
        self.m = YOLOv10.from_pretrained(f'jameslahm/{MODEL_ID}')
        
    def Propose(self, image: Image.Image):
        results = self.m.predict(source=image, imgsz=IMAGE_SIZE, conf=THRERSHOLD)
        names = results[0].names
        boxes = results[0].boxes
        annotations = [{"label": names[int(cl)], "conf": float(cf), "box": list([float(b) for b in box])} for cl, cf, box in zip(boxes.cls, boxes.conf, boxes.xyxy)]
        annotated_image = results[0].plot()
        return annotated_image[:, :, ::-1], annotations

if __name__ == "__main__":
    proposal = Proposal()
    image = "image/test1.jpg"
    image = Image.open(image, formats=["JPEG"])
    annotated_image, annotations = proposal.Propose(image)
    print(annotations)
    cv2.imshow("Annotated Image", annotated_image)
    cv2.waitKey(0)