import requests

def request_data():
    try:
        url = 'https://poe.ninja/poe1/api/economy/stash/current/currency/overview?league=Keepers&type=Currency'
        response = requests.get(url)
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error: Cannot request data from api: {e}")


