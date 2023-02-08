import clip
import torch
from PIL import Image


def init_model():
    global model, preprocess, device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device:", device)
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess, device


def predict(image, labels, model=None):
    if model is None:
        model, preprocess, device = init_model()

    image = preprocess(image).unsqueeze(0).to(device)
    text = clip.tokenize(labels).to(device)

    with torch.no_grad():
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()

    return probs
