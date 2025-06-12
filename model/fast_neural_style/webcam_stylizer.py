import cv2
import torch
import re
from torchvision import transforms
import numpy as np
from neural_style.transformer_net import TransformerNet
from PIL import Image

# Load the pre-trained model
model_path = 'saved_models/saved_models/candy.pth'  # <-- Change this to candy.pth or any model you want
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and map to device
style_model = TransformerNet()
state_dict = torch.load(model_path)
# Clean deprecated running stats
for k in list(state_dict.keys()):
    if re.search(r'in\d+\.running_(mean|var)$', k):
        del state_dict[k]
style_model.load_state_dict(state_dict)
style_model.to(device).eval()

# Preprocess image for model input
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(512),
    transforms.ToTensor(),
    transforms.Lambda(lambda x: x.mul(255))
])

# Postprocess image for OpenCV display
def postprocess(tensor):
    img = tensor.clone().detach().cpu().squeeze()
    img = img.numpy().transpose(1, 2, 0)
    img = np.clip(img, 0, 255).astype('uint8')
    return img

# Open webcam
cap = cv2.VideoCapture(0)
print("🎥 Webcam opened. Press 's' to stylize frame, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Live Webcam', frame)
    key = cv2.waitKey(1)

    if key == ord('s'):
        input_tensor = preprocess(frame).unsqueeze(0).to(device)
        with torch.no_grad():
            output_tensor = style_model(input_tensor)
        output_img = postprocess(output_tensor)
        cv2.imshow('Stylized Output', output_img)

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
