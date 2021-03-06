# k8s-Docker
### Prac_Kubernetes
--------------
## Kubernetes 설치 환경
  * Kubernetes 1.19.0
    * 1 Master Node, 1 Worker Node 
  * Nuclio 1.6.30
  * Docker 1:20.10.8
-----------------
## docker-registry pod&svc 설치 및 설정 과정
  1. docker-registry.yaml 만들기(위의 파일 이용)
    
  ```
  # yaml 파일 생성 후 아래의 명령어로 pod 및 svc 설치 진행 
    kubectl apply -f docker-registry.yaml
  ```
  2. 저장소 관련 설정
  ```
   vi /etc/docker/daemon.json
   "insecure-registries" : ["docker-registry.com:30500"]
   
   vi /etc/hosts
   192.168.56.31 docker-registry.com
  ```
-----------------
## Nuclio 설치 과정
  1. 필요 도구 설치
     ```
     # wget 도구 설치
     yum install wget
     
     # 최신 버전 helm 설치
     curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh
     chmod 700 get_helm.sh
     ./get_helm.sh
     helm repo add stable https://charts.helm.sh/stable
     helm repo update
     ```
  2. nuctl 설치 -> 전역에서 사용하기 위해 /usr/bin 으로 위치를 이동해서 설치를 진행(이것 말고도 export를 사용하는 방법도 있음) 
     ```
     wget https://github.com/nuclio/nuclio/releases/download/1.6.11/nuctl-1.6.11-linux-amd64
     chmod +x nuctl-1.6.11-linux-amd64
     mv nuctl-1.6.11-linux-amd64 nuctl
     ```
  3. nuclio 설치
      ```
      kubectl create namespace nuclio
    
      read -s mypassword
      # 비밀번호 입력하기(도커 저장소 비밀 번호 입력)
    
      kubectl --namespace nuclio create secret docker-registry registry-credentials \
      --docker-username 도커 아이디 입력 \
      --docker-password $mypassword \
      --docker-server registry.hub.docker.com  \
      --docker-email 도커 등록 이메일 입력
    
      # RBAC 파일 만들기(nuclio-rbac.yaml) -> 위의 파일 이용
      kubectl apply -f nuclio-rbac.yaml

      # nuclio 설치 파일 만들기(nuclio.yaml) -> 위의 파일 이용
      kubectl apply -f nuclio.yaml
    
      # 설치 확인(svc, pods)
      kubectl get svc --namespace=nuclio
      kubectl get pods --namespace=nuclio
    
      # 대시 보드 노드 포트로 expose -> 노드의 ip와 포트 번호를 이용해서 클러스터 외부에서 대시 보드 접근 가능
      kubectl expose deployment -n nuclio nuclio-dashboard --type=NodePort --name=nuclio-nodeport
      ```
      -----
      ## Docker 설치 (with Ubuntu)
      1. Set up the repository
      ```
      sudo apt-get update
      sudo apt-get upgrade
      ```
      2. Prerequisite package 설치
      ```
      sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
      ```
      3. Docker GPG key 추가
      ```
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
      ```
      4. stable 버전의 repository 설정
      ```
      echo \
        "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      ```
     5. Docker 엔진 설치
     ```
     sudo apt-get update
     sudo apt-get install docker-ce docker-ce-cli containerd.io
     ```
     6. 정상 설치 확인
     ```
     sudo docker run hello-world
     ```
