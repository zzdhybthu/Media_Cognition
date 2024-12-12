import torch
import clip
from PIL import Image
from constants import *

class Match():
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(MODEL_NAME, device=self.device)
        
    def Img2Txt(self, image: Image.Image, texts: list):
        image_feature = self.preprocess(image).unsqueeze(0).to(self.device)
        text_features = clip.tokenize(texts).to(self.device)
        with torch.no_grad():
            logits_per_image, _ = self.model(image_feature, text_features)
            probs = logits_per_image.softmax(dim=-1)
            max_prob, max_index = torch.max(probs, 1)
        return float(max_prob.cpu()), int(max_index.cpu())
    
    def Txt2Img(self, text: str, images: list):
        text_feature = clip.tokenize([text]).to(self.device)
        image_features = torch.stack(list(map(self.preprocess, images))).to(self.device)
        with torch.no_grad():
            _, logits_per_text = self.model(image_features, text_feature)
            probs = logits_per_text.softmax(dim=-1)
            max_prob, max_index = torch.max(probs, 1)
        return float(max_prob.cpu()), int(max_index.cpu())


if __name__ == "__main__":
    match = Match()
    
    max_prob, max_index = match.Img2Txt(Image.open("image/blue.jpg"), ["a box", "a rubbish bin", "a rubbish"])
    print("Max probability:", max_prob)
    print("Max index:", max_index)
    
    max_prob, max_index = match.Txt2Img("a blue bin", list(map(Image.open, ["image/gray.jpg", "image/green.jpg", "image/red.jpg", "image/blue.jpg"])))
    print("Max probability:", max_prob)
    print("Max index:", max_index)
