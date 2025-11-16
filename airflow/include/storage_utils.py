import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from io import BytesIO
from boto3.session import Session
from airflow.providers.postgres.hooks.postgres import PostgresHook

ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = 'ap-southeast-2'

def upload_data_to_s3(json_data):
    local_timezone = datetime.now(tz=ZoneInfo("Asia/Bangkok"))
    session = Session(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY
    )
    s3 = session.client("s3")
    bucket_name = 'poe1-currency-bucket'
    # file_name = f'currency_data-{timestamp}.json'
    file_name = f'poe1_currency/raw/{local_timezone:%Y/%m/%d/%H%M%S}'

    json_bytes = json.dumps(json_data).encode("utf-8")
    s3.upload_fileobj(BytesIO(json_bytes), bucket_name, file_name)


def upload_data_to_postgresql(exchange_df, currency_detail):
    postgres_hook = PostgresHook(postgres_conn_id='postgres_conn')
    
    listed_data = [(
        data['currency_id'],
        data['currency_name'],
        data['icon'],
        ) for index, data in currency_detail.iterrows()] 
    postgres_hook.insert_rows(
        table="dev.currency_metadata",
        rows=listed_data,
        target_fields=[
            "currency_id", "currency_name", "currency_icon"
        ],
        replace=False,
        replace_statement="""
            ON CONFLICT (currency_id, sample_time_local_time)
            DO NOTHING;
        """
    )
    
    listed_data = [(
        data['currency_id'],
        data['chaos_equivalent'],
        data['divine_equivalent'],
        data['sample_time_utc'],
        data['sample_time_local_time']  
        ) for index, data in exchange_df.iterrows()] 
    postgres_hook.insert_rows(
        table="dev.poe1_currency",
        rows=listed_data,
        target_fields=[
            "currency_id", "chaos_equivalent",
            "divine_equivalent", "sample_time_utc", "sample_time_local_time"
        ],
        replace=False,
        replace_statement="""
            ON CONFLICT (currency_id, sample_time_local_time)
            DO NOTHING;
        """
    )
    
