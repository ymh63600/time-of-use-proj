from fastapi import  Depends, APIRouter
from config import Response, Config
import pandas as pd
from connection import get_db
from sqlalchemy.orm.session import Session
from models import *
from datetime import datetime
from calculate_data.bill_type import *
import psycopg2

data_router = APIRouter()

start_date = datetime(2022, 5, 1, 0, 0, 0)  # 包含秒信息的起始日期时间
end_date = datetime(2022, 5, 30, 23, 59, 59)  # 包含秒信息的结束日期时间

conn = psycopg2.connect(Config.DB_URL)
cur = conn.cursor()

##date_time要改成你的table name
sql = f'''SELECT * FROM date_time WHERE device_uuid= %s AND generated_time BETWEEN %s AND %s'''


@data_router.get(
        "/calculate/test",
        tags=["Data"],
        summary="get pre_process data",
        description="get pre_process data",
        responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
        )
def pre_process_data(db: Session = Depends(get_db), uuid_example: str = "0bd0c50a-7847-4456-ba61-8e62a8af6f3b"):
    cur.execute(sql,(uuid_example, start_date, end_date,))
    data_from_db = cur.fetchall()

    mapped_data = [
        {
            "device_uuid": item[0],
            "generated_time": item[1],
            "normal_usage": item[2]
        }
        for item in data_from_db
    ]
    df = pd.DataFrame(mapped_data)

    # 3. 對 DataFrame 進行處理
    df['generated_time'] = pd.to_datetime(df['generated_time'])
    df['is_summer'] = df['generated_time'].apply(lambda x: 'summer' if x.month >= 6 and x.month <= 9 else 'non-summer')
    df['time_slot_type2'] = df.apply(categorize_time_slot_type2, axis=1)
    df['time_slot_type3'] = df.apply(categorize_time_slot_type3, axis=1)

    # 4. 對處理後的 DataFrame 進行按小時聚合並計算每小時使用量的差異
    df_hourly = df.groupby(pd.Grouper(key='generated_time', freq='h')).last()
    df_hourly['hourly_usage'] = df_hourly['normal_usage'].diff()
    df_hourly['hourly_usage'] = df_hourly['hourly_usage'].round(2)
    processed_data = df_hourly

    return processed_data

@data_router.get(
        "/calculate",
        tags=["Data"],
        summary="get electricity fee",
        description="get electricity fee",
        responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
        )
def calculate_electricity_fee(db: Session = Depends(get_db), uuid_example: str = "0bd0c50a-7847-4456-ba61-8e62a8af6f3b"):
    df = pre_process_data(db, uuid_example)
    summer_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type2'] == 'Weekday 9:00-24:00')]['hourly_usage'].sum()
    summer_off_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type2'] != 'Weekday 9:00-24:00')]['hourly_usage'].sum()
    non_summer_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type2'] == 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()
    non_summer_off_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type2'] != 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()

    # 計算電費類型1
    bill_type1 = (calculate_electricity_bill_type1(summer_peak_usage, summer_off_peak_usage)+
                calculate_electricity_bill_type1(non_summer_peak_usage, non_summer_off_peak_usage))

    # 計算電費類型2
    bill_type2 = (calculate_electricity_bill_type2(summer_peak_usage, summer_off_peak_usage, True) + 
                  calculate_electricity_bill_type2(non_summer_peak_usage, non_summer_off_peak_usage, False))

    # 計算夏季和非夏季的尖峰、半尖峰和離峰使用量
    summer_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type3'] == 'Weekday 16:00-22:00')]['hourly_usage'].sum()
    summer_semi_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type3'] == 'Weekday 09:00-16:00 22:00-24:00')]['hourly_usage'].sum()
    summer_off_peak_usage = df[(df['is_summer'] == 'summer') & ((df['time_slot_type3'] == 'Weekday 00:00-09:00') | (df['time_slot_type3'] == 'Weekend'))]['hourly_usage'].sum()
    non_summer_semi_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type3'] == 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()
    non_summer_off_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type3'] != 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()

    # 計算電費類型3
    bill_type3 = (calculate_electricity_bill_type3(summer_peak_usage, summer_off_peak_usage, summer_semi_peak_usage, True) + 
                  calculate_electricity_bill_type3(non_summer_peak_usage, non_summer_off_peak_usage, non_summer_semi_peak_usage, False))

    result_json = {
        # "summer_off_peak_usage" : summer_off_peak_usage,    
        # "summer_peak_usage" : summer_peak_usage,
        "bill_type1": bill_type1,
        "bill_type2": bill_type2,
        "bill_type3": bill_type3
    }

    return result_json

if __name__ == "__main__":
    print(calculate_electricity_fee())
   