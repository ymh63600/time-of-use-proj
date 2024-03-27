        
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