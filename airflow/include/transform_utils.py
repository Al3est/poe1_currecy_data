import pandas as pd

# import requests
# url = 'https://poe.ninja/poe1/api/economy/stash/current/currency/overview?league=Keepers&type=Currency'
# response = requests.get(url)
# json_data = response.json()

def df_transform(json_data):
    exchange_df = pd.DataFrame(columns=['currency_id', 'chaos_equivalent' ,'league', 'sample_time_utc'])
    for exchange_data in json_data['lines']:
        receive = exchange_data.get('receive', {})
        exchange_df.loc[len(exchange_df)] = [receive.get('get_currency_id'), exchange_data.get('chaosEquivalent'), 'Keepers', receive.get('sample_time_utc')]
    exchange_df['sample_time_utc'] = pd.to_datetime(exchange_df['sample_time_utc'])
    exchange_df['sample_time_local_time'] = exchange_df['sample_time_utc'].dt.tz_convert('Asia/Bangkok')


    currency_detail = pd.DataFrame(columns=['currency_id', 'currency_name','icon'])
    for currency_data in json_data['currencyDetails']:
        currency_detail.loc[len(currency_detail)] = [currency_data.get('id'), currency_data.get('name'), currency_data.get('icon')]

    return  exchange_df, currency_detail

def add_divine_equivalent(exchange_df):
    divine_price = exchange_df.loc[exchange_df['currency_id'] == 3, 'chaos_equivalent'].iloc[0]
    exchange_df['divine_equivalent'] = (exchange_df['chaos_equivalent']/divine_price).round(2)
    return exchange_df

# exchange_df, currency_detail  = df_transform(json_data)
# print(currency_detail.head())