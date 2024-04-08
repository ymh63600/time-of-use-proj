from datetime import datetime, timedelta
from fastapi import HTTPException, status,Request
from passlib.context import CryptContext
from jose import jwt
from config import Config
from models import User
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_token(username: str) -> str:

    access_token = jwt.encode(
        {
            "sub": username,
            "exp": datetime.utcnow()
            + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        Config.SECRET_KEY,
        algorithm=Config.ALGORITHM,
    )
    return access_token


def get_access_token(user: User, password: str) -> str:
    # use bcrypt algo. to verify password
    if not CryptContext(schemes=["bcrypt"], deprecated="auto").verify(
        password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    
    return generate_token(user.username)

def verify_password(plain_password, hashed_password):
    
    return pwd_context.verify(plain_password, hashed_password)

    
async def verify_token(request: Request):
    token=request.headers.get("Authorization","")
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return payload.get("sub")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

async def verify_admin(request: Request):
    admin = request.headers.get("is_Admin","")
    return admin

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template


def send_email(user: str,type: str):
    token = jwt.encode(
        {
            "sub": user,
            "exp": datetime.utcnow()
            + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        Config.SECRET_KEY,
        algorithm=Config.ALGORITHM,
    )
    content = MIMEMultipart()  #建立MIMEMultipart物件
     #郵件標題
    content["from"] = "timeofuse114@gmail.com"  #寄件者
    content["to"] = user #收件者
    if type == 'create':
        content["subject"] = "Mail verification" 
        template = Template(
            f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>
                Hello <strong>$user</strong>, your registration is almost success!
                Please click on <a href="http://localhost:3000/verification/{token}">this link</a> to complete email verification.
            </body>
            </html>
        """)
    else:
        content["subject"] = "Find password" 
        template = Template(
            f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>
                Hello <strong>$user</strong>!
                Please click on <a href="http://localhost:3000/find-password/{token}">this link</a> to update your new password.
            </body>
            </html>
        """)
    #http://localhost:8000/verification/?token={token}
    body = template.substitute({"user": user })
    content.attach(MIMEText(body, "html"))  # HTML郵件內容

    import smtplib
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("timeofuse114@gmail.com", Config.MAIL_KEY)  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)