import requests
import os
import json

def send_data(url):
    path_dir = '/root/pi'
    file_list = os.listdir(path_dir)
    for name in file_list:
        files = {
        #'file':open('C:\\Users\\ASUS\\Desktop\\hi\\hufs.jpg', 'rb')
            'file':open('/root/pi/' + name, 'rb')
        }
        res = requests.post(url,files=files)
        #name = res['name']
        res_json = res.json()
        if res_json['answer'] == "Detect":
            os.system("mv /root/pi/" + name + " /root/web" )
        else:
            os.system("rm -f /root/pi/"+ name)
    return "Done"

url = "http://192.168.56.31:32735/predict"
print(send_data(url))
