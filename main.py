import requests
import pprint
import os
import json
from typing import Any
from dotenv import load_dotenv

api_base_uri = "https://api.exchangerate.host"
currency_list_local_data = 'currency_code.json'

load_dotenv()
api_key = os.getenv("EX_API_KEY", "")

def check_file(path: str):
    return os.path.exists(path) and os.path.isfile(path)

def http_request_handler(uri: str):
    try:
        response = requests.get(uri)
        if response and response.status_code == 200:
            return response.json()
        else:
            print(f"error code: {response.status_code}, message: {response.content}")
    except Exception as e:
        print(str(e))
        return

def currency_list_frindly_output(currency_list: dict):
    for key, value in currency_list.items():
        print(f"{key}: {value}")

def currency_list_live() -> dict[Any, Any]:
    request_uri = f"{api_base_uri}/list?access_key={api_key}"
    json_data = http_request_handler(request_uri)
    pprint.pp(json_data)

def currency_list_local():
    with open(currency_list_local_data, 'rb') as f:
        currency_list = json.loads(f.read())
        currency_list_frindly_output(currency_list)

def currency_list_load():
    if check_file():
        currency_list_local
        return
    currency_list_live

def exchange_request() -> dict[Any, Any]:
    src_currency = input("Source currency: ")
    target_currency = input("Target currency: ")
    amount = input(f"{src_currency} Amount: ")
    request_uri = f"{api_base_uri}/convert?access_key={api_key}&from={src_currency}&to={target_currency}&amount={amount}"
    json_data = http_request_handler(request_uri)
    result = json_data.get('result')
    print(f"{target_currency} Amount: {result}")

if __name__ == "__main__":
    currency_list_local()
    exchange_request()
