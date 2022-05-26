import io
from pickletools import read_uint1
from torchvision import models
import json
from flask import Flask, jsonify, request
from flask import make_response
import torchvision.transforms as transforms
import torch
from PIL import Image
import os

app = Flask(__name__)

# yolo model 불러오기
model = torch.hub.load('./yolov5/', 'custom', path='./yolov5/runs/train/mask_check_models5/weights/best.pt', source='local')

# POST 통신으로 들어오는 이미지를 저장하고 모델로 추론하는 과정
def save_image(file):
    file.save('./temp/'+ file.filename)

@app.route('/')
def web():
    return "Hyun Do's flask test page"





@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        save_image(file) # 들어오는 이미지 저장
        train_img = './temp/' + file.filename
        temp = model(train_img)
        result = temp.pandas().xyxy[0]['name']
        check = True # 마스크 미착용 여부를 알려줄 변수
        answer = ""
        for i in range(len(result)):
            if result[i] == "no-mask":
                check = False
                answer = "Detect"
                break
        
        if check:
            answer = "Safe"
        
        res = {
            'answer' : answer
        }

        return res

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
