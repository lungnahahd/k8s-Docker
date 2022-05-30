from bs4 import BeautifulSoup
import requests
import os

url = 'http://swopenAPI.seoul.go.kr/api/subway/API 키 입력/xml/realtimePosition/0/100/2호선'
response = requests.get(url)

soup = BeautifulSoup(response.text,'lxml')

items = soup.find_all('row')

i = 0

for row in items:
    
    # print(f"호선 :{row.find('subwaynm').get_text()}")
    # print(f"현재 위치 :{row.find('statnnm').get_text()}")
    # print(f"열차번호 :{row.find('trainno').get_text()}")
    # print(i)
    # i += 1
    #print("-----------------------------------------------")

    # 위의 코드는 전체 열차에 대해 정보를 받기
    
    #아래의 코드는 특정 열차를 지정해서 위치를 받기
    if row.find('trainno').get_text() == "8292":
        print(f"현재 위치 : {row.find('statnnm').get_text()}")


### 아래는 단순 테스트 코드
path_dir = './picture'
file_list = os.listdir(path_dir)
for i in file_list:
    os.system("sshpass -p vagrant scp /home/pi/train_k8s/picture/" + i + " root@192.168.35.44:/root/pi")
os.system("sshpass -p vagrant ssh root@192.168.35.44 python /root/send.py")
