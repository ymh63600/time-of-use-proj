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
<html lang="en" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="normal">
<meta name="supported-color-schemes" content="normal">
<title>Mail verification</title>
</head>
<body class="body" >
    <!-- email content in here -->
    <table role="presentation" align="center" bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" width="100%">
		<tr>
			<td valign="top" bgcolor="#d5f8f4">
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.7em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center; padding-top:100px;">
									Hello, <strong>$user</strong> !
								</p >
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.5em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center;">
									We Are Almost There
								</p >
			<div class="over-mob"  style="max-height:340px; margin: 0 auto; text-align: center; ">
				<img class="reset" src="https://i.ibb.co/6ZB5zjp/frontend-web-2.png" width="300" height="200" border="0" alt="" style="vertical-align: middle;"/>
			</div>
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.5em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center;">
									Please Click on
				</p >
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.5em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center;">
        <a href="http://localhost:3000/verification/{token}">THIS LINK</a>
        </p >
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.5em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center;padding-bottom:100px;">
									To Verify Your Email.
				</p >
			<!-- TEXT BLOCK START -->
			</div>
				</td>
			</tr>
			</table>
			<div style="height: 40px;"></div>
			</td>
		</tr>
    </table>
  </div>
</body>
</html>
        """)
    else:
        content["subject"] = "Find password" 
        template = Template(
            f"""
            <!DOCTYPE html>
<html lang="en" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="normal">
<meta name="supported-color-schemes" content="normal">
<title>Find password</title>
</head>
<body class="body" >
    <!-- email content in here -->
    <table role="presentation" align="center" bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" width="100%">
		<tr>
			<td valign="top" bgcolor="#d5f8f4">
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.7em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center; padding-top:100px;">
									Hello, <strong>$user</strong> !
								</p >
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.5em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center;">
									Forgot Your Password?
				</p >
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.2em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center; padding-top:30px; opacity:50%;">
									That's okay, it happens!
				</p >
        
			<div class="over-mob"  style="max-height:340px; margin: 0 auto; text-align: center; ">
				<img class="reset" src="https://i.ibb.co/nrGRKrT/frontend-web-3.png" width="200" height="200" border="0" alt="" style="vertical-align: middle; "/>
			</div>
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.5em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center;">
									Please Click on
				</p >
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.5em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center;">
        <a href="http://localhost:3000/find-password/{token}">THIS LINK</a>
        </p >
        <p class="left" style="margin: 0; font-family:sans-serif; font-size:1.5em; color:#49688D; mso-line-height-rule: exactly; line-height: 1.5; text-align:center;padding-bottom:100px;">
									To Reset Your Password.
				</p >
			<!-- TEXT BLOCK START -->
			</div>
				</td>
			</tr>
			</table>
			<div style="height: 40px;"></div>
			</td>
		</tr>
    </table>
  </div>
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


if __name__ == "__main__":
    # use your email to test
    email = ""
    send_email(email,"find")
