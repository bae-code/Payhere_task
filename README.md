# Payhere_task

## ERD

----
![erd](erd.png)

----
### start.sh
```　
cd backend

pip install -r requirements.txt


python manage.py makemigrations


python manage.py migrate


python manage.py runserver
```

---

## API
path : /swagger


----
<table style="border-collapse: collapse; width: 100%; height: 210px;" border="1" data-ke-align="alignLeft" data-ke-style="style12">
<tbody>
<tr style="height: 19px;">
<td style="width: 25%; text-align: center; height: 19px;">기능</td>
<td style="width: 25%; text-align: center; height: 19px;">Method</td>
<td style="width: 25%; height: 19px; text-align: center;">URL</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;"><b>회원가입</b></td>
<td style="width: 25%; height: 17px;">POST</td>
<td style="width: 25%; height: 17px;">/user/register</td>
</tr>
<tr style="height: 19px;">
<td style="width: 25%; height: 19px;">로그인</td>
<td style="width: 25%; height: 19px;">POST</td>
<td style="width: 25%; height: 19px;">/user/login</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;">로그아웃 </td>
<td style="width: 25%; height: 17px;">POST</td>
<td style="width: 25%; height: 17px;">/user/logout</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;">가계부 작성</td>
<td style="width: 25%; height: 17px;">POST</td>
<td style="width: 25%; height: 17px;">/account-book/register</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;">가계부 수정</td>
<td style="width: 25%; height: 17px;">PUT</td>
<td style="width: 25%; height: 17px;">/account-book/{pk}</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;"><b>가계부 삭제</b></td>
<td style="width: 25%; height: 17px;">DELETE</td>
<td style="width: 25%; height: 17px;">/account-book/{pk}</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;">가계부 리스트</td>
<td style="width: 25%; height: 17px;">POST</td>
<td style="width: 25%; height: 17px;">/account-book/list</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;"><b>가계부 디테일</b></td>
<td style="width: 25%; height: 17px;">PUT</td>
<td style="width: 25%; height: 17px;">/account-book/{pk}</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;"><b>가계부 복제</b></td>
<td style="width: 25%; height: 17px;">POST</td>
<td style="width: 25%; height: 17px;">/account-book/clone/{pk}</td>
</tr>
<tr style="height: 17px;">
<td style="width: 25%; height: 17px;">가계부 공유 URL 생성</td>
<td style="width: 25%; height: 17px;">GET</td>
<td style="width: 25%; height: 17px;">/account-book/share/{pk}</td>
</tr>
<tr style="height: 19px;">
<td style="width: 25%; height: 19px;">가계부 통계</td>
<td style="width: 25%; height: 19px;">GET</td>
<td style="width: 25%; height: 19px;">account-book/stat</td>
</tr>
</tbody>
</table>

---

# API 설계

## User

---
### 회원가입
1. 유저는 name, email, password, password_check, phone 을 입력하여 회원가입 요청

    ~~~
    {
        "email":"test@payhere.kr",
        "name":"test",
        "password":"1234",
        "password_check":"1234",
        "phone":"01000000000"
    }
    ~~~

   1. password 와 password_check 가 다를 때
      ~~~
      HTTP 200 OK
       {
           "success":false,
           "msg": "비밀번호가 일치하지 않습니다."
       }
      ~~~

   2.  이미 존재 하는 Email 일때

      ~~~
      HTTP 400 Bad Request
    
    
      {
          "email": [
              "중복 이메일 입니다"
          ]
      }
      ~~~
2. 회원가입 완료 시 JWT 토큰을 발행 하고 쿠키를 생성 합니다.

3. 비밀번호는 암호화 되어 저장 됩니다.

### 로그인
1. 유저는 email과 password를 가지고 로그인 요청
~~~
{
    '"email":"test@payhere.kr",
    "password":"1234"
}
~~~
 
2. 로그인 완료시 JWT 토큰 발행과 쿠키 생성을 합니다.

### 로그아웃

1. 로그아웃 요청시 로그아웃과 쿠키에있는 token을 제거합니다.

--- 

## Account

