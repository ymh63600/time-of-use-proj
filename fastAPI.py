import pandas as pd
import os

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

def main(folder_path, filename):
    df = pd.read_csv(folder_path + filename, index_col='generated_time')

    summer_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type2'] == 'Weekday 9:00-24:00')]['hourly_usage'].sum()
    summer_off_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type2'] != 'Weekday 9:00-24:00')]['hourly_usage'].sum()
    non_summer_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type2'] == 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()
    non_summer_off_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type2'] != 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()

    bill_type1 = calculate_electricity_bill_type1(summer_peak_usage, summer_off_peak_usage)

    bill_type2 = (calculate_electricity_bill_type2(summer_peak_usage, summer_off_peak_usage, True) + 
                  calculate_electricity_bill_type2(non_summer_peak_usage, non_summer_off_peak_usage, False))

    summer_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type3'] == 'Weekday 16:00-22:00')]['hourly_usage'].sum()
    summer_semi_peak_usage = df[(df['is_summer'] == 'summer') & (df['time_slot_type3'] == 'Weekday 09:00-16:00 22:00-24:00')]['hourly_usage'].sum()
    summer_off_peak_usage = df[(df['is_summer'] == 'summer') & ((df['time_slot_type3'] == 'Weekday 00:00-09:00') | (df['time_slot_type3'] == 'Weekend'))]['hourly_usage'].sum()
    
    non_summer_semi_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type3'] == 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()
    non_summer_off_peak_usage = df[(df['is_summer'] == 'non-summer') & (df['time_slot_type3'] != 'Weekday 6:00-11:00 14:00-24:00')]['hourly_usage'].sum()

    bill_type3 = (calculate_electricity_bill_type3(summer_peak_usage, summer_off_peak_usage, summer_semi_peak_usage, True) + 
                  calculate_electricity_bill_type3(non_summer_peak_usage, non_summer_off_peak_usage, non_summer_semi_peak_usage, False))

    # print("原本電價:" ,bill_type1)
    # print("二段式電費試算價格:" ,bill_type2)
    # print("三段式電費試算價格:", bill_type3)

    result = pd.DataFrame({'電價類別': ['原本電價', '二段式電費試算價格', '三段式電費試算價格'],
                           '總費用': [bill_type1, bill_type2, bill_type3]})
    
    output_filename = "output/electricity_fee/" + filename + "_fee.csv"
    result.to_csv(output_filename, index=False)

if __name__ == "__main__":
    folder_path = "output/pre_processing_dataset/"  # Specify the folder path containing the files
    # folder_path = "output/test/"
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        main(folder_path, file_name)



    '''
    # summer_usages = float(input("夏月每月用電度數（單位：度）："))
    # peak_percentage = float(input("尖峰比例（%）："))
    # semi_peak_percentage = float(input("半尖峰比例（%）："))
    # off_peak_percentage = float(input("離峰比例（%）："))


    # non_summer_usages = float(input("非夏月每月用電度數（單位：度）："))
    # peak_percentage = float(input("尖峰比例（%）："))
    # semi_peak_percentage = float(input("半尖峰比例（%）："))
    # off_peak_percentage = float(input("離峰比例（%）："))
   
    # bill_type1 = calculate_electricity_bill_type1(summer_usages, non_summer_usages)
    # bill_type2 = (calculate_electricity_bill_type2(summer_usages * (peak_percentage + semi_peak_percentage), summer_usages * off_peak_percentage, True) + 
    # calculate_electricity_bill_type2(non_summer_usages * (peak_percentage + semi_peak_percentage), non_summer_usages * off_peak_percentage, False ))
    # bill_type3 = (calculate_electricity_bill_type3(summer_usages * peak_percentage, summer_usages * semi_peak_percentage, summer_usages * off_peak_percentage, True) + 
    # calculate_electricity_bill_type3(non_summer_usages * peak_percentage, non_summer_usages * semi_peak_percentage, non_summer_usages * off_peak_percentage, False ))
    '''