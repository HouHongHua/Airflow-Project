# Airflow Project: TSMC Stock Price DAGs

這個專案使用 **Apache Airflow** 自動抓取台灣台積電（2330.TW）的股票資料，並可透過 DAG 定時或手動運行來處理資料。專案採用 **Docker + Docker Compose** 部署，方便管理與維護。

---

## 專案目標

- 每天自動抓取 TSMC 股價資料（開盤價、收盤價等）。
- 支援手動觸發 DAG 以測試或立即抓取資料。
- 使用自訂 Docker 映像與 requirements.txt 管理 Python 套件。

---

## 專案結構

```text
airflow/
├── dags/                  # DAG 定義檔
│   └── tsmc.py
├── logs/                  # Airflow 執行 log
├── plugins/               # 自訂插件（如有）
├── config/                # Airflow 設定檔或 .env
├── requirements.txt       # Python 套件需求
├── Dockerfile             # 自訂 Airflow Docker 映像
└── docker-compose.yaml    # Docker Compose 設定
