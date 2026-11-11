import json
import os
import pprint
import sys
from typing import Any

from dotenv import load_dotenv
import requests

api_base_uri = "https://api.exchangerate.host"
currency_code_json_file_path = ""
currency_code_json_file_name = "currency_code.json"
common_pairs_json_file_path = ""
common_pairs_json_file_name = "common_pairs.json"
api_key = ""

DEFAULT_COMMON_PAIRS = [
    {"name": "TWD 轉 USD", "from": "TWD", "to": "USD"},
    {"name": "USD 轉 TWD", "from": "USD", "to": "TWD"},
    {"name": "JPY 轉 TWD", "from": "JPY", "to": "TWD"},
    {"name": "TWD 轉 JPY", "from": "TWD", "to": "JPY"},
    {"name": "EUR 轉 TWD", "from": "EUR", "to": "TWD"},
    {"name": "USD 轉 JPY", "from": "USD", "to": "JPY"},
]


def get_exec_path() -> str:
    """取得執行路徑 (相容原始碼執行與 PyInstaller 打包環境)"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    script_invocation_path = sys.argv[0]
    return os.path.dirname(os.path.abspath(script_invocation_path))


def check_file(path: str) -> bool:
    return os.path.exists(path) and os.path.isfile(path)


def http_request_handler(
    uri: str,
    params: dict[str, Any] | None = None,
    allow_redirects: bool = False,
    timeout: int = 10,
) -> dict[str, Any] | None:
    """發送 HTTP 請求並安全解析 JSON 回應"""
    try:
        response = requests.get(
            uri,
            params=params,
            allow_redirects=allow_redirects,
            timeout=timeout,
        )

        # 檢測重定向 (例如 exchangerate.host 將未授權或非付費端點 301 重定向至文檔 HTML 頁面)
        if response.status_code in (301, 302, 303, 307, 308):
            return None

        # 檢查 Rate Limit
        if response.status_code == 429:
            print("[API Warning] HTTP 429: Too Many Requests. API 呼叫頻率已達上限，請稍候重試。")
            return None

        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            # 若不是 JSON 內容類型 (例如重定向後收到的 HTML 頁面)
            if "application/json" not in content_type:
                print(f"[API Error] Expected JSON but received Content-Type: '{content_type}'.")
                return None

            try:
                data = response.json()
            except (json.JSONDecodeError, ValueError) as json_err:
                print(f"[API Error] Failed to parse JSON: {json_err}")
                return None

            if isinstance(data, dict) and data.get("success") is False:
                err = data.get("error", {})
                print(f"[API Error] Code {err.get('code')}: {err.get('info')}")
                return None

            return data
        else:
            print(f"[HTTP Error] Status code: {response.status_code}, content: {response.text[:200]}")
            return None

    except requests.exceptions.Timeout:
        print(f"[Network Error] Request timed out ({timeout}s).")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[Network Error] Request failed: {e}")
        return None
    except Exception as e:
        print(f"[Unexpected Error] {e}")
        return None


def currency_list_friendly_output(currency_list: dict):
    for key, value in currency_list.items():
        print(f"{key}: {value}")


# 保留原始打字筆誤名稱以維持相容性
currency_list_frindly_output = currency_list_friendly_output


def currency_list_live(show_list: bool = False) -> dict[Any, Any] | None:
    request_uri = f"{api_base_uri}/list"
    json_data = http_request_handler(request_uri, params={"access_key": api_key})
    if not json_data or not isinstance(json_data, dict):
        print("Failed to fetch live currency list from API.")
        return None

    currencies = json_data.get("currencies")
    if not currencies or not isinstance(currencies, dict):
        print("No valid currencies found in API response.")
        return None

    if show_list:
        currency_list_friendly_output(currencies)
    try:
        with open(currency_code_json_file_path, "w", encoding="utf-8") as f:
            json.dump(currencies, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Warning: Could not save currency list to file: {e}")
    return currencies


def currency_list_local(show_list: bool = True) -> bool:
    try:
        with open(currency_code_json_file_path, "r", encoding="utf-8") as f:
            currency_list = json.load(f)
            if isinstance(currency_list, dict):
                if show_list:
                    currency_list_friendly_output(currency_list)
                return True
    except Exception as e:
        print(f"Warning: Failed to read local currency file: {e}")
    return False


def currency_list_load(show_list: bool = False):
    if check_file(currency_code_json_file_path) and currency_list_local(show_list=show_list):
        return
    currency_list_live(show_list=show_list)


def load_common_pairs() -> list[dict[str, str]]:
    """讀取常用的幣別轉換表，若檔案不存在則自動建立預設檔案"""
    if not check_file(common_pairs_json_file_path):
        try:
            with open(common_pairs_json_file_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_COMMON_PAIRS, f, indent=4, ensure_ascii=False)
            return DEFAULT_COMMON_PAIRS
        except IOError as e:
            print(f"Warning: Failed to create default {common_pairs_json_file_name}: {e}")
            return DEFAULT_COMMON_PAIRS

    try:
        with open(common_pairs_json_file_path, "r", encoding="utf-8") as f:
            pairs = json.load(f)
            if isinstance(pairs, list):
                return pairs
    except Exception as e:
        print(f"Warning: Failed to read {common_pairs_json_file_name}: {e}")
    return DEFAULT_COMMON_PAIRS


def select_currency_pair() -> tuple[str, str]:
    """顯示常用幣別選單供數字選擇，或支援手動輸入"""
    pairs = load_common_pairs()

    while True:
        if pairs:
            print("=== 常用幣別轉換 (Quick Currency Exchange) ===")
            for idx, pair in enumerate(pairs, start=1):
                name = pair.get("name") or f"{pair.get('from')} 轉 {pair.get('to')}"
                print(f"[{idx}] {name}")
            print("[0] 自訂輸入幣別 (Custom Currency)")
            print("[L] 查詢所有支援幣別清單 (List All Currencies)")
            print("==============================================")

            choice = input(f"請選擇 (1-{len(pairs)}, 0=自訂, L=清單) [預設: 1]: ").strip()
            if not choice:
                choice = "1"

            if choice.upper() == "L":
                print("\n--- 支援幣別代碼清單 ---")
                currency_list_local(show_list=True)
                print("-----------------------\n")
                continue

            if choice == "0":
                break

            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(pairs):
                    sel = pairs[idx - 1]
                    src = sel.get("from", "").strip().upper()
                    dst = sel.get("to", "").strip().upper()
                    if src and dst:
                        return src, dst
                else:
                    print(f"輸入無效，請輸入 1 到 {len(pairs)} 或 0。\n")
                    continue
            else:
                print("輸入格式不正確，請輸入數字或 L。\n")
                continue
        else:
            break

    # 自訂手動輸入
    src_currency = input("Source currency: ").strip().upper()
    target_currency = input("Target currency: ").strip().upper()
    return src_currency, target_currency


def convert_via_live_quotes(src_currency: str, target_currency: str, amount: float) -> float | None:
    """備援方案：當 /convert 端點受限時，利用 /live 即時匯率進行換算"""
    request_uri = f"{api_base_uri}/live"
    json_data = http_request_handler(request_uri, params={"access_key": api_key})
    if not json_data or not isinstance(json_data, dict):
        return None

    quotes = json_data.get("quotes", {})
    if not quotes or not isinstance(quotes, dict):
        print("No exchange rate quotes available in live data.")
        return None

    # /live 報價基底為 USD，格式如 'USDAED', 'USDTWD'
    usd_to_src = 1.0 if src_currency == "USD" else quotes.get(f"USD{src_currency}")
    usd_to_target = 1.0 if target_currency == "USD" else quotes.get(f"USD{target_currency}")

    if usd_to_src is None:
        print(f"Error: Unknown or unsupported source currency '{src_currency}'.")
        return None
    if usd_to_target is None:
        print(f"Error: Unknown or unsupported target currency '{target_currency}'.")
        return None

    # 交叉匯率計算
    rate = usd_to_target / usd_to_src
    return amount * rate


def exchange_request() -> dict[Any, Any] | None:
    src_currency, target_currency = select_currency_pair()

    if not src_currency or not target_currency:
        print("Error: Currency codes cannot be empty.")
        return None

    amount_str = input(f"{src_currency} Amount: ").strip()

    try:
        amount = float(amount_str)
    except ValueError:
        print(f"Error: Invalid amount '{amount_str}'. Please enter a valid number.")
        return None

    # 先嘗試呼叫 /convert 端點 (付費方案或支援該端點時)
    request_uri = f"{api_base_uri}/convert"
    params = {
        "access_key": api_key,
        "from": src_currency,
        "to": target_currency,
        "amount": amount,
    }
    json_data = http_request_handler(request_uri, params=params, allow_redirects=False)

    if json_data and isinstance(json_data, dict):
        result = json_data.get("result")
        if result is not None:
            print(f"{target_currency} Amount: {result}")
            return json_data

    # 若 /convert 端點無法使用 (例如免費方案 301 重定向至說明頁)，自動切換至 /live 匯率計算
    converted_amount = convert_via_live_quotes(src_currency, target_currency, amount)
    if converted_amount is not None:
        print(f"{target_currency} Amount: {converted_amount:.4f}")
    else:
        print("Failed to complete currency exchange.")
    return None


if __name__ == "__main__":
    exec_dir_path = get_exec_path()
    currency_code_json_file_path = os.path.join(exec_dir_path, currency_code_json_file_name)
    common_pairs_json_file_path = os.path.join(exec_dir_path, common_pairs_json_file_name)
    load_dotenv(os.path.join(exec_dir_path, ".env"))
    api_key = os.getenv("EX_API_KEY", "")
    if not api_key:
        print("Warning: EX_API_KEY is not set or empty in .env.")
    currency_list_load(show_list=False)
    exchange_request()
