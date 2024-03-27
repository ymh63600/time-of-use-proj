from fastapi import  Depends, APIRouter, Form
from config import Response
import pandas as pd
from connection import get_db
from sqlalchemy.orm.session import Session
from models import *
from sqlalchemy import and_
from datetime import datetime
from calculate_data.bill_type import *

data_router = APIRouter()

start_date = datetime(2022, 1, 9, 0, 0, 0)  # 包含秒信息的起始日期时间
end_date = datetime(2023, 1, 9, 23, 59, 59)  # 包含秒信息的结束日期时间

@data_router.get(
        "/calculate/test",
        tags=["Data"],
        summary="get pre_process data",
        description="get pre_process data",
        responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
        )
def pre_process_data(db: Session = Depends(get_db)):
    uuid_example = "0bd0c50a-7847-4456-ba61-8e62a8af6f3b"
    data_from_db = db.query(Electricity_Data).filter(
        and_(
            Electricity_Data.device_uuid == uuid_example,
            Electricity_Data.generated_time >= start_date,
            Electricity_Data.generated_time <= end_date
        )
    ).all()
    data_dict = [{'device_uuid': item.device_uuid, 'generated_time': item.generated_time, 'normal_usage': item.normal_usage} for item in data_from_db]
    df = pd.DataFrame(data_dict)

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
    # 5. 返回處理後的結果（您可以根據需要返回 df_hourly 或其他格式的數據）
    # processed_data.to_csv('processed_data.csv', index=True)
    return processed_data

@data_router.get(
        "/calculate",
        tags=["Data"],
        summary="get electricity fee",
        description="get electricity fee",
        responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},
        )
def calculate_electricity_fee(db: Session = Depends(get_db)):
    df = pre_process_data(db)
    summer_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type2'] == 'Weekday 9:00-24:00')]['hourly_usage'].sum()
    summer_off_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type2'] != 'Weekday 9:00-24:00')]['hourly_usage'].sum()
    non_summer_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type2'] == 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()
    non_summer_off_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type2'] != 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()

    # 計算電費類型1
    bill_type1 = calculate_electricity_bill_type1(summer_peak_usage, summer_off_peak_usage)

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
        "bill_type1": bill_type1,
        "bill_type2": bill_type2,
        "bill_type3": bill_type3
    }

    return result_json
   