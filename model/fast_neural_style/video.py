import cv2
import torch
import re
from torchvision import transforms
import numpy as np
from neural_style.transformer_net import TransformerNet

# Load model as before (your code)
model_path = 'saved_models/saved_models/rain_princess.pth'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

style_model = TransformerNet()
state_dict = torch.load(model_path)
for k in list(state_dict.keys()):
    if re.search(r'in\d+\.running_(mean|var)$', k):
        del state_dict[k]
style_model.load_state_dict(state_dict)
style_model.to(device).eval()

preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(512),
    transforms.ToTensor(),
    transforms.Lambda(lambda x: x.mul(255))
])

def postprocess(tensor):
    img = tensor.clone().detach().cpu().squeeze()
    img = img.numpy().transpose(1, 2, 0)
    img = np.clip(img, 0, 255).astype('uint8')
    return img

# Video input and output
video_path = 'input1.mp4'
cap = cv2.VideoCapture(video_path)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter('stylized_output.mp4', fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    input_tensor = preprocess(frame).unsqueeze(0).to(device)
    with torch.no_grad():
        output_tensor = style_model(input_tensor)
    output_img = postprocess(output_tensor)

    out.write(output_img)
    cv2.imshow('Stylized Video', output_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
