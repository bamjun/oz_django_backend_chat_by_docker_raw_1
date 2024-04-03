# 유튜브 백엔드 구현

## 1. REST API
### (1) 모델 구조
1. User (Custom)
    - email(user_id)
    - password
    - nickname
    - is_business(Boolean) : personal, business

#### (1) User Model 생성
- docker-compose run --rm app sh -c 'django-admin startapp users'
- app.settings 수정 (AUTH_USER_MODEL = 'users.User' 추가, INSTALLED_APPS = 'users.apps.UsersConfig' 추가)
- UserModel 작성 (AbstactBaseModel 상속)
- makemigrations -> migrate 해서 db 적용

2. Video
    - title
    - link
    - description
    - thumbnail
    - video_uploaded_url (S3)
    - video_file(FileField)
    - category
    - views_count
    - User : FK
    - reactions (좋아요, 싫어요 기능)
    
3. Like/Dislike
    - Video : FK (Video : 1, Like/Dislike : n)
    - User : FK
    
4. Subscription
    - User : FK => Subscriber(구독자)
    - User : FK => Subscribed_to

5. Comment
    - Video : FK
    - User : FK
    - like
    - dislike
    - content

6. Notification
    - message
    - is_read (읽었는지 여부 : Boolean)
    - User : FK

7. Common
    - Created_at
    - Updated_at
## AWS 배포
### IAM 사용자 생성
1. 생성하기 버튼
2. 사용자 이름 입력, 직접생성 비밀번호 입력
3. 권한정책 직접 선택 -> AdministratorAccess 선택 후 생성

### AWS key-pair create
1. 터미널에서 ssh-keygen -t rsa -b 4096 입력 후 경로에 파일이름 입력 후 비밀번호 입력
2. cat 키페어파일이름.pub 명령어로 파일열어서 키값 복사

### EC2 인스턴스 생성 후 연결
1. EC2 이름 입력
2. amazon Linux 2023 AMI 이미지 선택 (프리티어)
3. 키페어 선택
4. 보안 그룹 생성 -> 인터넷에서 HTTP 트래픽 허용 체크
5. 인스턴스 시작
6. 인스턴스에 연결 클릭
7. 터미널에 ssh-add 키페어파일이름 입력해서 ssh에 키페어 연결
8. ssh ec2-user@복사한 퍼블릭 ipv4 주소 입력해서 ssh 접속
9. ssh-keygen -t ed25519 -b 4096 입력해서 키젠 생성
10. cd .ssh -> ls -al -> id_ed25519.pub 파일존재 확인 후 cat 명령어로 열기
11. 값을 복사해서 깃허브 레포지토리 - settings - Deploy keys - add deploy key 에서 키값에 붙여넣기 후 생성
12. 터미널에 sudo yum install git -y  입력해서 EC2에 git 설치
13. 터미널에 sudo yum install docker -y  입력해서 EC2에 docker 설치
14. sudo systemctl start docker 도커 실행 명령어
15. sudo systemctl enable docker 시스템 링크를 만들어서 운영가능한 상태로 만들어줌. 시스템 부팅 시 알아서 실행해줌
16. sudo usermod -aG docker ec2-user : ec2-user에 도커 그룹을 추가한다.
17. exit해서 종료후 다시실행해서 권한 적용시켜주기
18. sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose 명령어 실행해서 docker-compose 명령어 사용가능하도록 install 시켜주기
19. cd /usr/local/bin 로 이동
20. ls -al 명령어로 docker-compose 존재 확인
21. sudo chmod +x docker-compose : 슈퍼유저 권한으로 docker-compose 라는 명령어를 실행
22. cd ~ 로 최상위폴더이동
23. git clone https://github.com/Meoyoug/django-backend-youtube.git 깃 클론해오기
24. cd django-backend-youtube 로 클론한 폴더로 이동
25. vim .env 명령어로 .env 파일 생성
26. 
```vim
DB_HOST=db
DB_NAME=name
DB_USER=user
DB_PASS=pass
SECRET_KEY=key
ALLOWED_HOSTS=(EC2의 퍼블릭 IPv4 DNS - 배포후에 이쪽으로 접속해줘야하기 때문)
```
입력하고 wq하고 저장
27. 장고 settings.py에 CORS_ALLOWED_ORIGINS = [
    'EC2 ipv4 도메인주소 입력'
]
28. docker-compose -f docker-compose-deploy.yml build 명령어로 빌드
29. docker-compose -f docker-compose-deploy.yml up 명령어로 서버실행
