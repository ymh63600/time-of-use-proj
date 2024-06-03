import os
import psycopg2
import csv
import pandas as pd

# PostgreSQL 資料庫參數
DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'postgres'
DB_USER = 'myuser'
DB_PASS = 'mypassword'

# 連接到 PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
conn.autocommit = False
cur = conn.cursor()

# Get all file names in the 'dataset/' directory
file_names = os.listdir('dataset/convert_dataset')

# For each file name
for file_name in file_names:
    table_name = file_name.replace('.csv', '')
    file_path = 'dataset/convert_dataset/' + file_name
    print(table_name)

    # 读取CSV文件，舍弃第一列
    df = pd.read_csv(file_path, usecols=['generated_time', 'normal_usage'], dtype={'generated_time': str, 'normal_usage': float})            

     # 将 generated_time 列的数据类型转换为 datetime
    df['generated_time'] = pd.to_datetime(df['generated_time'], errors='coerce')
    
    # 过滤掉任何包含 NaT 的行
    df = df.dropna(subset=['generated_time'])

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        generated_time TIMESTAMP,
        normal_usage FLOAT
    );
    """

    temp_file_path = f'dataset/temp_{file_name}'
    df.to_csv(temp_file_path, index=False, header=False, date_format='%Y-%m-%d %H:%M:%S')

    cur.execute(create_table_query)

    # 使用COPY命令插入数据
    with open(temp_file_path, 'r') as f:
        cur.copy_expert(f"COPY {table_name} (generated_time, normal_usage) FROM STDIN WITH CSV", f)

    # 删除临时文件
    os.remove(temp_file_path)

# Commit the changes
conn.commit()