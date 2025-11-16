import sys
from datetime import timedelta
from airflow.sdk import dag, task
from airflow.providers.standard.operators.python import PythonOperator


sys.path.append('/opt/airflow/include')
from api_utils import request_data
from transform_utils import df_transform, add_divine_equivalent
from storage_utils import upload_data_to_s3, upload_data_to_postgresql

@dag(schedule=timedelta(hours=1), catchup=False)
def poe1_currrency_dag():

    @task
    def request_task():
        json_data = request_data()
        return json_data
    
    @task
    def upload_raw_task_s3(json_data):
        upload_data_to_s3(json_data)
    
    @task(multiple_outputs=True)
    def convert_to_df(json_data):
        exchange_df, currency_detail = df_transform(json_data)
        return {
            "exchange_df": exchange_df,
            "currency_detail": currency_detail
        }

    @task
    def add_divine(exchange_df):
        return add_divine_equivalent(exchange_df)
    
    @task
    def upload_data_postgre(exchange_df, currency_detail):
        upload_data_to_postgresql(exchange_df, currency_detail)
    
    
    json_data = request_task()
    # upload_raw_task_s3(json_data)
    converted_df = convert_to_df(json_data)
    exchange_df = converted_df["exchange_df"] 
    currency_detail = exchange_df["currency_detail"]
    exchange_df = add_divine(exchange_df)
    upload_data_postgre(exchange_df, currency_detail)

poe1_currrency_dag()
