import requests

def send_data(url):
    files = {
        'file':open('C:\\Users\\ASUS\\Desktop\\hi\\image2.jpg', 'rb')
    }
    res = requests.post(url,files=files)
    return res.text

url = "http://192.168.56.30:5000/predict"
print(send_data(url))
