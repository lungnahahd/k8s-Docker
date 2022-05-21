import io
from torchvision import models
import json
from flask import Flask, jsonify, request
from flask import make_response
import torchvision.transforms as transforms
from PIL import Image

app = Flask(__name__)

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)
    

# 이미 학습된 가중치를 사용하기 위해 `pretrained` 에 `True` 값을 전달
model = models.densenet121(pretrained=True)

# 모델을 추론에만 사용할 것이므로, `eval` 모드로 변경
model.eval()

# ImageNet 분류 ID와 ImageNet 분류명의 쌍 정보
imagenet_class_index = json.load(open('imagenet_class_index.json'))

def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)  # i.에서 정의
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    
    return imagenet_class_index[predicted_idx]
    


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # 전달받은 request에서 이미지 데이터 받고 byte로 변환
        file = request.files['file']
        img_bytes = file.read()
        
        # 추론값 생성
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        
        # response로 전달할 데이터 생성
        answer = "이 동물은 %s 입니다"%(class_name)
        
        # 주의!! #
        # jsonify를 사용하면 json.dump()와 똑같이 ascii 인코딩을 사용하기 때문에 한글 깨짐
        # return jsonify({'class_id': class_id, 'class_name': class_name})
        
        # 이 방법으로 response 전달해야 함(!!!!)
        res = {
            'class_id' : class_id,
            'class_name' : class_name,
            'answer' : answer
        }
        res = make_response(json.dumps(res, ensure_ascii=False))
        res.headers['Content-Type'] = 'application/json'
        
        return res
    
if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
