from fastapi import FastAPI, UploadFile, File
import pandas as pd
from config import Response

app = FastAPI()

@app.post(
        "/uploadcsv/",
        tags=["Data"],
        summary="upload csv file",
        description="upload csv file",
        responses={200: Response.OK.doc, 400: Response.BAD_REQUEST.doc},)
def create_upload_file(file: UploadFile = File(...), start_time: str = None, end_time: str = None):
    df = convert_file(file, start_time, end_time)
    
    summer_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type2'] == 'Weekday 9:00-24:00')]['hourly_usage'].sum()
    summer_off_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type2'] != 'Weekday 9:00-24:00')]['hourly_usage'].sum()
    non_summer_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type2'] == 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()
    non_summer_off_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type2'] != 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()

    bill_type1 = (calculate_electricity_bill_type1(summer_peak_usage, summer_off_peak_usage)+
                calculate_electricity_bill_type1(non_summer_peak_usage, non_summer_off_peak_usage))

    bill_type2 = (calculate_electricity_bill_type2(summer_peak_usage, summer_off_peak_usage, True) + 
                  calculate_electricity_bill_type2(non_summer_peak_usage, non_summer_off_peak_usage, False))

    summer_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type3'] == 'Weekday 16:00-22:00')]['hourly_usage'].sum()
    summer_semi_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type3'] == 'Weekday 09:00-16:00 22:00-24:00')]['hourly_usage'].sum()
    summer_off_peak_usage = df[(df['is_summer'] == 'summer') & ((df['time_slot_type3'] == 'Weekday 00:00-09:00') | (df['time_slot_type3'] == 'Weekend'))]['hourly_usage'].sum()
    
    non_summer_semi_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type3'] == 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()
    non_summer_off_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type3'] != 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()

    bill_type3 = (calculate_electricity_bill_type3(summer_peak_usage, summer_off_peak_usage, summer_semi_peak_usage, True) + 
                  calculate_electricity_bill_type3(non_summer_peak_usage, non_summer_off_peak_usage, non_summer_semi_peak_usage, False))

    print("原本電價:" ,bill_type1)
    print("二段式電費試算價格:" ,bill_type2)
    print("三段式電費試算價格:", bill_type3)
    
    return {"type1": bill_type1, "type2": bill_type2, "type3": bill_type3}

def calculate_electricity_bill_type1(summer_usage, non_summer_usage): 
    total = summer_usage + non_summer_usage
    if(total <= 120):
        total_cost = total * 1.63
    elif(121 <= total <= 330):
        total_cost = summer_usage * 2.38 + non_summer_usage * 2.1
    elif(331 <= total <= 500):
        total_cost = summer_usage * 3.52 + non_summer_usage * 2.89
    elif(501 <= total <= 700):
        total_cost = summer_usage * 4.8 + non_summer_usage * 3.94
    elif(701 <= total <= 1000):
        total_cost = summer_usage * 5.83 + non_summer_usage * 4.74
    else:
        total_cost = summer_usage * 7.69 + non_summer_usage * 6.03
    return int(total_cost)

def calculate_electricity_bill_type2(peak_usage, off_peak_usage, is_summer):  
    if is_summer:
        peak_rate = 4.71  # 尖峰時段
        off_peak_rate = 1.85
    else:
        peak_rate = 4.48  #離峰時段
        off_peak_rate = 1.78
    
    if peak_usage + off_peak_usage > 2000:
        peak_rate += 0.99
        off_peak_rate += 0.99
    
    #基本電費75
    total_cost = (peak_usage * peak_rate + off_peak_usage * off_peak_rate ) + 75
    return int(total_cost)

def calculate_electricity_bill_type3(peak_usage, off_peak_usage, semi_peak_usage, is_summer):
    if is_summer:
        peak_rate = 6.49  # 尖峰時段
        semi_peak_rate = 4.26
        off_peak_rate = 1.85
    else:
        peak_rate = 0  #離峰時段
        semi_peak_rate = 4.06
        off_peak_rate = 1.78
    
    if peak_usage + semi_peak_usage + off_peak_usage > 2000:
        peak_rate += 0.99
        semi_peak_rate += 0.99
        off_peak_rate += 0.99
    
    #基本電費75
    total_cost = (peak_usage * peak_rate + semi_peak_usage * semi_peak_rate + off_peak_usage * off_peak_rate) + 75
    return int(total_cost)

def categorize_time_slot_type2(row):
    if row['is_summer'] == 'summer':
        if row['generated_time'].weekday() < 5 and (row['generated_time'].hour >= 9 and row['generated_time'].hour < 24):
            return 'Weekday 9:00-24:00'
        elif row['generated_time'].weekday() < 5 and (row['generated_time'].hour >= 0 and row['generated_time'].hour < 9):
            return 'Weekday 00:00-09:00'
        else:
            return 'Weekend'
    else:
        if row['generated_time'].weekday() < 5 and ((row['generated_time'].hour >= 6 and row['generated_time'].hour < 11) or (row['generated_time'].hour >= 14 and row['generated_time'].hour < 24)):
            return 'Weekday 6:00-11:00 14:00-24:00'
        elif row['generated_time'].weekday() < 5 and ((row['generated_time'].hour >= 0 and row['generated_time'].hour < 6) or (row['generated_time'].hour >= 11 and row['generated_time'].hour < 14)):
            return 'Weekday 00:00-06:00 11:00-14:00'
        else:
            return 'Weekend'
      
def categorize_time_slot_type3(row):
    if row['is_summer'] == 'summer':
        if row['generated_time'].weekday() < 5 and (row['generated_time'].hour >= 16 and row['generated_time'].hour < 22):
            return 'Weekday 16:00-22:00'
        elif row['generated_time'].weekday() < 5 and (row['generated_time'].hour >= 0 and row['generated_time'].hour < 9):
            return 'Weekday 00:00-09:00'
        elif row['generated_time'].weekday() < 5 and ((row['generated_time'].hour >= 9 and row['generated_time'].hour < 16) or (row['generated_time'].hour >= 22 and row['generated_time'].hour < 24)):
            return 'Weekday 09:00-16:00 22:00-24:00'
        else:
            return 'Weekend'
    else:
        if row['generated_time'].weekday() < 5 and ((row['generated_time'].hour >= 6 and row['generated_time'].hour < 11) or (row['generated_time'].hour >= 14 and row['generated_time'].hour < 24)):
            return 'Weekday 06:00-11:00 14:00-24:00'
        elif row['generated_time'].weekday() < 5 and ((row['generated_time'].hour >= 0 and row['generated_time'].hour < 6) or (row['generated_time'].hour >= 11 and row['generated_time'].hour < 14)):
            return 'Weekday 00:00-06:00 11:00-14:00'
        else:
            return 'Weekend'

# Function to convert each file
def convert_file(file: UploadFile, start_time: str, end_time: str):
    df = pd.read_csv(file)
    
    # Convert the 'generated_time' column to datetime
    df['generated_time'] = pd.to_datetime(df['generated_time'])
    # Select data between start_time and end_time
    df = df[(df['generated_time'] >= start_time) & (df['generated_time'] <= end_time)]

    df['is_summer'] = df['generated_time'].apply(lambda x: 'summer' if x.month >= 6 and x.month <= 9 else 'non-summer')
    df['time_slot_type2'] = df.apply(categorize_time_slot_type2, axis=1)
    df['time_slot_type3'] = df.apply(categorize_time_slot_type3, axis=1)
    
    # Group by hourly frequency and take the last row of each hour
    df_hourly = df.groupby(pd.Grouper(key='generated_time', freq='h')).last()

    # Calculate the difference in normal_usage between consecutive hours
    df_hourly['hourly_usage'] = df_hourly['normal_usage'].diff()
    df_hourly['hourly_usage'] = df_hourly['hourly_usage'].round(5)
    
    return df_hourly

if __name__ == "__main__":
    file_path = r'dataset\0bd0c50a-7847-4456-ba61-8e62a8af6f3b.csv'
    start_time = '2022-05-01 00:00:00'
    end_time = '2022-05-31 23:59:59'

    with open(file_path, "rb") as file:
        create_upload_file(file=file, start_time=start_time, end_time=end_time)