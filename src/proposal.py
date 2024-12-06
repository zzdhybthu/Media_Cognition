from ultralytics import YOLOv10
from constants import *
import cv2
from PIL import Image
import numpy as np
import os


class Proposal():
    def __init__(self):
        # if os.path.exists("./yolov10n.pt"):
        #     self.m = YOLOv10.from_pretrained("yolov10n.pt", cache_dir='.')
        # else:
        #     self.m = YOLOv10.from_pretrained(f'jameslahm/{MODEL_ID}')
        self.m = YOLOv10('yolov10s.pt')
    
    def Propose4(self, image: Image.Image, return_image=False):
        predicts = []
        for degree in [0, 90, 180, 270]:
            rotated_image = image.rotate(degree)
            _, annotations = self.Propose(rotated_image)
            predicts.append({
                "deg": degree,
                "ann": annotations
            })
            
        # rotate box back
        w, h = image.size
        delta = (h - w) / 2
        for p in predicts:
            for a in p["ann"]:
                box = a["box"]
                if p["deg"] == 270:
                    a["box"] = [box[1] - delta, h - box[2] - delta, box[3] - delta, h - box[0] - delta]
                elif p["deg"] == 180:
                    a["box"] = [w - box[2], h - box[3], w - box[0], h - box[1]]
                elif p["deg"] == 90:
                    a["box"] = [w - box[3] + delta, box[0] + delta, w - box[1] + delta, box[2] + delta]
                    
        # merge boxes with same label
        ann_merged = []
        for p in predicts:
            for a in p["ann"]:
                found = False
                for m in ann_merged:
                    if m["label"] == a["label"]:
                        m["box"].append(a["box"])
                        m["conf"].append(a["conf"])
                        found = True
                        break
                if not found:
                    ann_merged.append({
                        "label": a["label"],
                        "box": [a["box"]],
                        "conf": [a["conf"]]
                    })
        for m in ann_merged:
            m["box"] = np.mean(m["box"], axis=0)
            m["conf"] = np.mean(m["conf"])
        predicts = ann_merged
        
        annotated_image = None
        if return_image:
            annotated_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
            for pi, p in enumerate(predicts):
                box = p["box"]
                cv2.rectangle(annotated_image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), colors[pi % len(colors)], 2)
                cv2.putText(annotated_image, f"{p['label']} {p['conf']:.2f}", (int(box[0]), int(box[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[pi % len(colors)], 2)
                
        return annotated_image, predicts
        
        
    def Propose(self, image: Image.Image, return_image=False):
        results = self.m.predict(source=image, imgsz=IMAGE_SIZE, conf=THRERSHOLD)
        names = results[0].names
        boxes = results[0].boxes
        annotations = [{"label": names[int(cl)], "conf": float(cf), "box": list([float(b) for b in box])} for cl, cf, box in zip(boxes.cls, boxes.conf, boxes.xyxy)]
        annotated_image = None
        if return_image:
            annotated_image = results[0].plot()
        return annotated_image, annotations

if __name__ == "__main__":
    proposal = Proposal()
    image = "image/test4.jpg"
    image = Image.open(image, formats=["JPEG"])
    image = image.convert("RGB")
    annotated_image, annotations = proposal.Propose(image, return_image=True)
    print(annotations)
    cv2.imshow("Annotated Image", annotated_image)
    cv2.waitKey(0)