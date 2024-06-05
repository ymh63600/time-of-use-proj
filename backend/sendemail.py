from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from datetime import datetime, timedelta
from jose import jwt
from config import Config
import smtplib
import pandas as pd

def send_nilm_email(user: str,type: str):
    # token = jwt.encode(
    #     {
    #         "sub": user,
    #         "exp": datetime.utcnow()
    #         + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
    #     },
    #     Config.SECRET_KEY,
    #     algorithm=Config.ALGORITHM,
    # )
    content = MIMEMultipart()  #建立MIMEMultipart物件
     #郵件標題
    content["from"] = "timeofuse114@gmail.com"
    content["to"] = user
    content["subject"] = "Nilm Advice" 

    template = Template(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>NILM Advice</title>
            <style>
                body, html {
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                }
                .container {
                    width: 100%;
                    height: 100%;
                    background-color: #ffffff;
                }
                .header, .footer {
                    text-align: left;
                    width: 100%;
                }
                .header img, .footer img {
                    width: 100%;
                    max-width: 800px;
                    height: auto;
                }
                .content {
                    padding: 20px;
                    text-align: left;
                }
                .content p {
                    font-size: 1.2em;
                    color: #49688D;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img src="https://i.ibb.co/1TCDKTS/frontend-web-1-copy.png" alt="Header Image">
                </div>
                <div class="content">
                    <p>$advice</p>
                </div>
                <div class="footer">
                    <img src="https://i.ibb.co/nsSCmkC/frontend-web-1-copy-2.png" alt="Footer Image">
                </div>
            </div>
        </body>
        </html>
        """
    )

    advice = get_advice()
    print(advice)
    advice = advice.replace('\n', '<br>')

    body = template.substitute({"advice": advice})
    # body = template.substitute({"user": user})
    content.attach(MIMEText(body, "html"))
    
    #寄送郵件
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("timeofuse114@gmail.com", Config.MAIL_KEY)  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)

def get_advice(filename: str = "1970-01-26_1970-01-28.csv"):
    appliances = ["dish washer", "electric stove", "light", "microwave", "electric space heater", "electric oven"]
    
    start_time = '1970-01-26 07:30:00' 
    end_time = '1970-01-27 07:30:00'
    df = pd.read_csv(filename, parse_dates=[0], index_col=0)
    df = df.loc[start_time:end_time]
    # print(df.head())
    advice  = "二段式電價建議：\n"
    advice += bill_2_advice(df, appliances, "1970-01-26", "1970-01-27")
    advice += "\n" + "="*50 + "\n\n"
    advice += "三段式電價建議：\n"
    advice += bill_3_advice(df, appliances, "1970-01-26", "1970-01-27")
    
    return advice
    

def bill_2_advice(df, appliances, start_date, end_date):
    advice = ""
    time_periods = [("07:30:00", "10:30:00"), ("10:30:00", "20:30:00"), ("16:00:00", "22:30:00")]

    for start_time_suffix, end_time_suffix in time_periods:
        start_time = start_date + " " + start_time_suffix
        end_time = end_date + " " + end_time_suffix
        df = df.loc[start_time:end_time]
        df = df > 0
        advice_appliance1 = ""
        advice_appliance2 = ""
        for appliance in appliances:
            usage_time = df[appliance].sum() * 1
            if usage_time >= 10:
                if start_time_suffix == time_periods[0][0]:
                    advice_appliance1 += appliance + "、"
                elif start_time_suffix == time_periods[1][0] and appliance in ["electric stove", "microwave", "electric oven"]:
                    advice += f"建議您外出就餐或者買便當吃，以避開電價尖峰時間。\n"
                    break
                elif start_time_suffix == time_periods[2][0] and appliance not in ["electric stove", "microwave", "electric oven"]:
                    advice_appliance2 += appliance + "、"
    
    if(advice_appliance1 != ""):
        advice_appliance1 = advice_appliance1[:-1]
        advice += f"建議您在7:30以前使用{advice_appliance1}，以避開7:30之後的電價尖峰時間。\n"
    if(advice_appliance2 != ""):
        advice_appliance2 = advice_appliance2[:-1]
        advice += f"建議您在晚上22:30之後使用{advice_appliance2}，以避開晚上22:30之前的電價尖峰時間。\n"
    return advice


def bill_3_advice(df, appliances, start_date, end_date):
    advice = ""
    time_periods = [("07:30:00", "10:00:00"), ("10:00:00", "12:00:00"), ("13:00:00", "17:00:00"), ("16:00:00", "17:00:00"), ("17:00:00", "22:30:00")]

    for start_time_suffix, end_time_suffix in time_periods:
        start_time = start_date + " " + start_time_suffix
        end_time = end_date + " " + end_time_suffix
        df = df.loc[start_time:end_time]
        df = df > 0
        advice_appliance1 = ""
        advice_appliance2 = ""
        advice_appliance3 = ""
        advice_appliance4 = ""
        advice_appliance5 = ""

        advice_2 = False
        for appliance in appliances:
            usage_time = df[appliance].sum() * 1
            if usage_time >= 10:
                if start_time_suffix == time_periods[0][0]:
                    advice_appliance1 += appliance + "、"
                elif start_time_suffix == time_periods[1][0] and appliance in ["electric stove", "microwave", "electric oven"]:
                    advice_2 = True
                elif start_time_suffix == time_periods[1][0] and appliance not in ["electric stove", "microwave", "electric oven"]:
                    advice_appliance2 += appliance + "、"
                elif start_time_suffix == time_periods[2][0] and appliance not in ["electric stove", "microwave", "electric oven"]:
                    advice_appliance3 += appliance + "、"
                elif start_time_suffix == time_periods[3][0] and appliance in ["electric stove", "microwave", "electric oven"]:
                    advice_appliance4 += appliance + "、"
                elif start_time_suffix == time_periods[4][0] and appliance not in ["electric stove", "microwave", "electric oven"]:
                    advice_appliance5 += appliance + "、"
    
    if(advice_appliance1 != ""):
        advice_appliance1 = advice_appliance1[:-1]
        advice += f"建議您在7:30以前使用{advice_appliance1}，以避開7:30之後的電價尖峰時間。\n"
    if(advice_appliance2 != ""):
        advice_appliance2 = advice_appliance2[:-1]
        advice += f"建議您在早上10:00以前或中午12:00之後使用{advice_appliance2}，以避開中午（10:00-12:00）之間的電價尖峰時間。\n"
    if advice_2:
        advice += f"建議您外出就餐或者買便當吃，以避開電價尖峰時間。\n"
    if(advice_appliance3 != ""):
        advice_appliance3 = advice_appliance3[:-1]
        advice += f"建議您在中午13:00以前或傍晚17:00之後使用{advice_appliance4}，以避開（13:00-17:00）之間的電價尖峰時間。\n"
    if(advice_appliance4 != ""):
        advice_appliance4 = advice_appliance4[:-1]
        advice += f"建議在傍晚17:00之後使用{advice_appliance4}，以避開晚餐時間的電價尖峰時間。\n"
    if(advice_appliance5 != ""):
        advice_appliance5 = advice_appliance5[:-1]
        advice += f"建議您在晚上22:30之後使用{advice_appliance5}，以避開晚上22:30之前的電價尖峰時間。\n"
    return advice



if __name__ == "__main__":
    send_nilm_email("esthersoon2002@gmail.com", "type")
    # get_advice()