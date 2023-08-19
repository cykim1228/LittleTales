import torch
from ultralytics import YOLO
import ultralytics

print(torch.cuda.is_available())

if __name__ == '__main__':
    model = YOLO('yolov8n.pt')
    model.train(data='D:\yolo\Fish-44\data.yaml', imgsz=640, batch=2, epochs=30)