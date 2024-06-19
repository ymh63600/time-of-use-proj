from nilmtk.dataset_converters import convert_redd
import os
import psycopg2
import pandas as pd
from config import Config_Time


# PostgreSQL 資料庫參數
DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'postgres'
DB_USER = 'myuser'
DB_PASS = 'mypassword'

def export_data(id_min=None, id_max=None):

    # 建立 fetch_data 目錄
    os.makedirs('fetch_data', exist_ok=True)
    house_dir = os.path.join('fetch_data', 'house_1')
    os.makedirs(house_dir, exist_ok=True)

    # 建立連接
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

    # 建立游標
    cur = conn.cursor()

    # 讀取 labels 表的所有數據
    df_labels = pd.read_sql('SELECT * FROM labels', conn)

    # 將 labels 表的數據寫入 .dat 文件
    df_labels.to_csv(os.path.join(house_dir, 'labels.dat'), index=False, header=False, sep=' ')

    # 對每個表執行相同的操作
    for i in range(1, 16):
        table_name = f'channel_{i}'

    # 根據 id 的範圍來建立 SQL 查詢語句
        if id_min is not None and id_max is not None:
            sql_query = f'SELECT * FROM {table_name} WHERE time BETWEEN {id_min} AND {id_max}'
        else:
            sql_query = f'SELECT * FROM {table_name}'

        # 讀取數據
        df = pd.read_sql(sql_query, conn)

        # 將數據寫入 .dat 文件
        df.to_csv(os.path.join(house_dir, f'{table_name}.dat'), index=False, header=False, sep=' ')

        print("===" + table_name + " complete ===")

    # 關閉連接
    cur.close()
    conn.close()

def get_h5(start_date,days):

    last_fetch_time = start_date * 24 * 60 * 60
    days = days
    interval = days * 24 * 60 * 60 # 秒數
    
    export_data(last_fetch_time, last_fetch_time + interval)
    convert_redd(r'fetch_data', f'data_h5/house_1_{start_date}.h5')

    

if __name__ == '__main__':
    
    get_h5(Config_Time.start_date,1)

    