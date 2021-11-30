# 💳Payhere-assignment

<br>

## ⚒️ 기술 환경 및 tools
---
- Python 3.9
- Django 3.2.9
- MySQL 8.0.26
- AWS
  - EC2
  - RDS 5.7.26
- Docker
- Git
- Github
- Postman

<br>
<br>

## 📋 ERD 및 DDL
---

- ERD : `/docs/payhere.drawio.png` 참고
- DDL : `/src/payhere.sql` 참고

<br>
<br>

## ➡️ Local 실행 방법(mac OS 기준)
---

- `my_settings.py` 생성
```py
# my_settings.py

## < > 부분은 직접 입력
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'payhere',
        'USER': 'root',
        'PASSWORD': <PASSWORD>,
        'HOST': 'localhost,
        'PORT': '3306',
    }
}

SECRET_KEY = <SECRET_KEY>

ALGORITHM = 'HS256'

SESSION_TIME_OUT = 10 * 60
```

- github 연동
```shell
$ git clone https://github.com/Oraange/Payhere-assignment.git
```

- Server 실행
```shell
$ ls
Dockerfile       manage.py        requirements.txt
README.md        my_settings.py   payhere          

$ python manage.py runserver
```

<br>
<br>

## 🐳Docker 실행 방법(mac OS 기준)
---

```shell
$ ls
Dockerfile       manage.py        requirements.txt
README.md        my_settings.py   payhere   

$ docker pull hrpp1300/payhere:0.1.1

$ docker run --name <container name> -d -p 8000:8000 hrpp1300/payhere:0.1.1
```

<br>
<br>

## 🔖 API Document
---


https://documenter.getpostman.com/view/17231503/UVJeEFWv

> API에 대한 설명은 여기에 자세히 나와있습니다.

<br>
<br>

## 🌲 디렉토리 구조
---

```
.
├── Dockerfile
├── README.md
├── account_books
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── dto.py
│   ├── exceptions.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── service.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_create.py
│   │   ├── test_delete.py
│   │   ├── test_get_detail.py
│   │   ├── test_get_list.py
│   │   ├── test_restore.py
│   │   ├── test_trash_list.py
│   │   └── test_update.py
│   ├── urls.py
│   └── views.py
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── authorizations.py
│   ├── exceptions.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── service.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── docs
│   ├── CONVENTION.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── payhere.drawio.png
├── manage.py
├── my_settings.py
├── payhere
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── src
│   └── payhere.sql
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── dto.py
    ├── exceptions.py
    ├── migrations
    │   └── 0001_initial.py
    ├── models.py
    ├── service.py
    ├── tests
    │   ├── __init__.py
    │   ├── test_log_out.py
    │   ├── test_sign_in.py
    │   └── test_sign_up.py
    ├── urls.py
    ├── validations.py
    └── views.py
```

<br>
<br>

## 👉 기능 설명
---

**자세한 API 명세는 [API Document](https://documenter.getpostman.com/view/17231503/UVJeEFWv)를 통해 확인할 수 있습니다.**

### User

<br>

> UUID를 사용하여 유저의 아이디 정보를 최대한 복잡하게 설계하였습니다.

<br>

  - 회원가입
    - email과 password, nick name을 입력하여 회원가입을 진행하고 중복된 email이 존재할 경우 예외 발생

  - 로그인
    - 가입된 정보를 가지고 로그인을 하여 email과 password가 일치하면 jwt 발급
    - 로그인시 cookie에 session id 저장

  - 로그아웃
    - 로그아웃을 요청하면 cookie에 저장된 session id를 삭제
    - session에는 만료 시간이 존재하여 해당 시간이 경과한 후 session key가 삭제됨 -> 로그인 페이지로 redirect

<br>

### Account Book

<br>

> - 가계부 정보에 대한 CRUD입니다.
> - 유저의 인증을 거쳐야 API 호출이 가능합니다.
> - login decorator를 통해 유저 인가를 해줍니다.
> - session만료시 로그인 페이지로 redirect됩니다.

<br>

- 가계부 생성
  - `type`은 1(수입) 또는 2(지출)만 입력 가능 (그 외의 값 입력시 예외 발생)
- 가계부 수정
  - 선택한 가계부의 정보를 입력한 값으로 수정
- 가계부 조회
  - 해당 유저의 가계부 전체 목록 및 상세 정보 조회 가능
- 가계부 삭제
  - 선택한 가계부를 삭제
- 가계부 삭제 목록 조회
  - 해당 유저가 삭제한 가계부 목록 조회
- 가계부 복구
  - 삭제된 가계부를 복구하는 기능
