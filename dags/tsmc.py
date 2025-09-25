from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import yfinance as yf
import pandas as pd
import os

def fetch_save_tsmc_data():
    """
    抓台積電當天開盤價與收盤價 印在Airflow log 儲存為 CSV 檔案
    """
    ticker = yf.Ticker("2330.TW")

    # 建立一個存放資料的資料夾
    data_folder = "/opt/airflow/data"
    os.makedirs(data_folder, exist_ok=True)
    
    # 取得當天資料，period="1d" 表示最近 1 天
    data = ticker.history(period="1d", interval="5m")

    if not data.empty:
        # 未收盤會用最近價格
        open_price = data['Open'].iloc[-1]
        close_price = data['Close'].iloc[-1]
        print(f"TSMC 開盤價：{open_price} TWD")
        print(f"TSMC 收盤價：{close_price} TWD") 

        # 將 DataFrame 儲存為 CSV 檔案
        filename = f"tsmc_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = os.path.join(data_folder, filename)
        
        data.to_csv(file_path)
        print(f"台積電當日報價已成功儲存至 {file_path}")
    else:
        print("沒有抓到資料")

# DAG 設定
with DAG(
    dag_id="Daily_TSMC_Prices",
    start_date=datetime(2025, 9, 24),   # 可以改成過去日期測試
    schedule_interval="@daily",          # 每天自動執行
    catchup=False,                       # 不補跑過去日期
    tags=["finance"],
) as dag:

    task_fetch_prices = PythonOperator(
        task_id="fetch_save_tsmc_data",
        python_callable=fetch_save_tsmc_data,
    )