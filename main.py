import requests
import pprint
import os
import sys
import json

from typing import Any
from dotenv import load_dotenv

api_base_uri = "https://api.exchangerate.host"
currency_code_json_file_path = ''
currency_code_json_file_name = 'currency_code.json'

load_dotenv()
api_key = os.getenv("EX_API_KEY", "")

def get_exec_path() -> str:
    # Get the path used to invoke the script
    script_invocation_path = sys.argv[0]

    # Get the absolute path of the script
    absolute_script_path = os.path.abspath(script_invocation_path)

    # Get the directory containing the script
    return os.path.dirname(absolute_script_path)

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
    currencies = json_data.get('currencies')
    currency_list_frindly_output(currencies)
    with open(currency_code_json_file_path, 'w') as f:
        json.dump(currencies, f, indent=4)

def currency_list_local():
    with open(currency_code_json_file_path, 'rb') as f:
        currency_list = json.loads(f.read())
        currency_list_frindly_output(currency_list)

def currency_list_load():
    if check_file(currency_code_json_file_path):
        currency_list_local()
        return
    currency_list_live()

def exchange_request() -> dict[Any, Any]:
    src_currency = input("Source currency: ")
    target_currency = input("Target currency: ")
    amount = input(f"{src_currency} Amount: ")
    request_uri = f"{api_base_uri}/convert?access_key={api_key}&from={src_currency}&to={target_currency}&amount={amount}"
    json_data = http_request_handler(request_uri)
    result = json_data.get('result')
    print(f"{target_currency} Amount: {result}")

if __name__ == "__main__":
    exec_dir_path = get_exec_path()
    currency_code_json_file_path = f"{exec_dir_path}/{currency_code_json_file_name}"
    currency_list_load()
    exchange_request()
