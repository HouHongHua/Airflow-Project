from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

with DAG(
    dag_id="test_postgres_dag",
    start_date=datetime(2025, 9, 24),
    schedule_interval=None,    # 手動觸發
    catchup=False,
    tags=["test"],
) as dag:

    # 建立 users 表
    create_table = PostgresOperator(
        task_id="create_users_table",
        postgres_conn_id="postgres",  # ⚠️ 確保 Airflow Connection 裡有這個 ID
        sql="""
            CREATE TABLE IF NOT EXISTS public.users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            );
        """,
    )

    # 插入測試資料
    insert_user = PostgresOperator(
        task_id="insert_test_user",
        postgres_conn_id="postgres",
        sql="""
            INSERT INTO public.users (firstname, lastname, country, username, password, email)
            VALUES ('Bruce', 'Wayne', 'USA', 'batman', 'darkknight', 'bruce@wayne.com');
        """,
    )

    # 查詢資料並在 log 顯示
    select_users = PostgresOperator(
        task_id="select_users",
        postgres_conn_id="postgres",
        sql="SELECT * FROM public.users;",
        do_xcom_push=True,  # ⚠️ 這樣查詢結果會寫進 XCom
    )

    create_table >> insert_user >> select_users
