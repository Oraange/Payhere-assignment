# π³Payhere-assignment

<br>

## βοΈ κΈ°μ  νκ²½ λ° tools
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

## π ERD λ° DDL
---

- ERD : `/docs/payhere.drawio.png` μ°Έκ³ 
- DDL : `/src/payhere.sql` μ°Έκ³ 

<br>
<br>

## β‘οΈ Local μ€ν λ°©λ²(mac OS κΈ°μ€)
---

- `my_settings.py` μμ±
```py
# my_settings.py

## < > λΆλΆμ μ§μ  μλ ₯
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

- github μ°λ
```shell
$ git clone https://github.com/Oraange/Payhere-assignment.git
```

- Server μ€ν
```shell
$ ls
Dockerfile       manage.py        requirements.txt
README.md        my_settings.py   payhere          

$ python manage.py runserver
```

<br>
<br>

## π³Docker μ€ν λ°©λ²(mac OS κΈ°μ€)
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

## π API Document
---


https://documenter.getpostman.com/view/17231503/UVJeEFWv

> APIμ λν μ€λͺμ μ¬κΈ°μ μμΈν λμμμ΅λλ€.

<br>
<br>

## π² λλ ν λ¦¬ κ΅¬μ‘°
---

```
.
βββ Dockerfile
βββ README.md
βββ account_books
βΒ Β  βββ __init__.py
βΒ Β  βββ admin.py
βΒ Β  βββ apps.py
βΒ Β  βββ dto.py
βΒ Β  βββ exceptions.py
βΒ Β  βββ migrations
βΒ Β  βΒ Β  βββ __init__.py
βΒ Β  βββ models.py
βΒ Β  βββ service.py
βΒ Β  βββ tests
βΒ Β  βΒ Β  βββ __init__.py
βΒ Β  βΒ Β  βββ test_create.py
βΒ Β  βΒ Β  βββ test_delete.py
βΒ Β  βΒ Β  βββ test_get_detail.py
βΒ Β  βΒ Β  βββ test_get_list.py
βΒ Β  βΒ Β  βββ test_restore.py
βΒ Β  βΒ Β  βββ test_trash_list.py
βΒ Β  βΒ Β  βββ test_update.py
βΒ Β  βββ urls.py
βΒ Β  βββ views.py
βββ core
βΒ Β  βββ __init__.py
βΒ Β  βββ admin.py
βΒ Β  βββ apps.py
βΒ Β  βββ authorizations.py
βΒ Β  βββ exceptions.py
βΒ Β  βββ migrations
βΒ Β  βΒ Β  βββ __init__.py
βΒ Β  βββ models.py
βΒ Β  βββ service.py
βΒ Β  βββ tests.py
βΒ Β  βββ urls.py
βΒ Β  βββ views.py
βββ docs
βΒ Β  βββ CONVENTION.md
βΒ Β  βββ PULL_REQUEST_TEMPLATE.md
βΒ Β  βββ payhere.drawio.png
βββ manage.py
βββ my_settings.py
βββ payhere
βΒ Β  βββ __init__.py
βΒ Β  βββ asgi.py
βΒ Β  βββ settings.py
βΒ Β  βββ urls.py
βΒ Β  βββ wsgi.py
βββ requirements.txt
βββ src
βΒ Β  βββ payhere.sql
βββ users
    βββ __init__.py
    βββ admin.py
    βββ apps.py
    βββ dto.py
    βββ exceptions.py
    βββ migrations
    βΒ Β  βββ 0001_initial.py
    βββ models.py
    βββ service.py
    βββ tests
    βΒ Β  βββ __init__.py
    βΒ Β  βββ test_log_out.py
    βΒ Β  βββ test_sign_in.py
    βΒ Β  βββ test_sign_up.py
    βββ urls.py
    βββ validations.py
    βββ views.py
```

<br>
<br>

## π κΈ°λ₯ μ€λͺ
---

**μμΈν API λͺμΈλ [API Document](https://documenter.getpostman.com/view/17231503/UVJeEFWv)λ₯Ό ν΅ν΄ νμΈν  μ μμ΅λλ€.**

### User

<br>

> UUIDλ₯Ό μ¬μ©νμ¬ μ μ μ μμ΄λ μ λ³΄λ₯Ό μ΅λν λ³΅μ‘νκ² μ€κ³νμμ΅λλ€.

<br>

  - νμκ°μ
    - emailκ³Ό password, nick nameμ μλ ₯νμ¬ νμκ°μμ μ§ννκ³  μ€λ³΅λ emailμ΄ μ‘΄μ¬ν  κ²½μ° μμΈ λ°μ

  - λ‘κ·ΈμΈ
    - κ°μλ μ λ³΄λ₯Ό κ°μ§κ³  λ‘κ·ΈμΈμ νμ¬ emailκ³Ό passwordκ° μΌμΉνλ©΄ jwt λ°κΈ
    - λ‘κ·ΈμΈμ cookieμ session id μ μ₯

  - λ‘κ·Έμμ
    - λ‘κ·Έμμμ μμ²­νλ©΄ cookieμ μ μ₯λ session idλ₯Ό μ­μ 
    - sessionμλ λ§λ£ μκ°μ΄ μ‘΄μ¬νμ¬ ν΄λΉ μκ°μ΄ κ²½κ³Όν ν session keyκ° μ­μ λ¨ -> λ‘κ·ΈμΈ νμ΄μ§λ‘ redirect

<br>

### Account Book

<br>

> - κ°κ³λΆ μ λ³΄μ λν CRUDμλλ€.
> - μ μ μ μΈμ¦μ κ±°μ³μΌ API νΈμΆμ΄ κ°λ₯ν©λλ€.
> - login decoratorλ₯Ό ν΅ν΄ μ μ  μΈκ°λ₯Ό ν΄μ€λλ€.
> - sessionλ§λ£μ λ‘κ·ΈμΈ νμ΄μ§λ‘ redirectλ©λλ€.

<br>

- κ°κ³λΆ μμ±
  - `type`μ 1(μμ) λλ 2(μ§μΆ)λ§ μλ ₯ κ°λ₯ (κ·Έ μΈμ κ° μλ ₯μ μμΈ λ°μ)
- κ°κ³λΆ μμ 
  - μ νν κ°κ³λΆμ μ λ³΄λ₯Ό μλ ₯ν κ°μΌλ‘ μμ 
- κ°κ³λΆ μ‘°ν
  - ν΄λΉ μ μ μ κ°κ³λΆ μ μ²΄ λͺ©λ‘ λ° μμΈ μ λ³΄ μ‘°ν κ°λ₯
- κ°κ³λΆ μ­μ 
  - μ νν κ°κ³λΆλ₯Ό μ­μ 
- κ°κ³λΆ μ­μ  λͺ©λ‘ μ‘°ν
  - ν΄λΉ μ μ κ° μ­μ ν κ°κ³λΆ λͺ©λ‘ μ‘°ν
- κ°κ³λΆ λ³΅κ΅¬
  - μ­μ λ κ°κ³λΆλ₯Ό λ³΅κ΅¬νλ κΈ°λ₯
