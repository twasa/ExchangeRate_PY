# Exchange rate implement with Python

A lightweight Python currency exchange rate CLI tool powered by [exchangerate.host](https://exchangerate.host).

## Features
- **Quick Currency Pair Selection**: Choose frequently used currency pairs with a single number key.
- **Customizable Configuration**: Customize favorite currency pairs in `common_pairs.json`.
- **Automatic Fallback**: Transparently calculates rates via `/live` when `/convert` is restricted on free-tier API keys.
- **Offline Currency List Cache**: Caches 170+ currency codes locally to `currency_code.json`.

## Requirements
- Package manager: [uv](https://github.com/astral-sh/uv)
- API Key: [exchangerate.host](https://exchangerate.host/signup/free) API key (free tier supported)

## Installation & Setup
1. Sync dependencies with `uv`:
```shell
uv sync
```

2. Configure API Key:
Create a `.env` file in the project directory:
```env
EX_API_KEY="your_api_key_here"
```
Or set the environment variable:
- **Unix**: `export EX_API_KEY="your_api_key_here"`
- **Windows (PowerShell)**: `$ENV:EX_API_KEY="your_api_key_here"`

## Run
```shell
uv run python main.py
```

## Build to Binary
- **Windows**:
```ps1
./build.ps1
```
- **Unix**:
```shell
./build.sh
```

The compiled standalone executable will be placed in the `dist/` directory.

## Configuration: `common_pairs.json`
You can customize frequently used currency pairs by editing `common_pairs.json` (auto-generated on first run):
```json
[
  {
    "name": "TWD 轉 USD",
    "from": "TWD",
    "to": "USD"
  },
  {
    "name": "USD 轉 TWD",
    "from": "USD",
    "to": "TWD"
  }
]
```

## Input and Output Examples

### Quick Selection (e.g. Option 1: TWD to USD)
```txt
=== 常用幣別轉換 (Quick Currency Exchange) ===
[1] TWD 轉 USD
[2] USD 轉 TWD
[3] JPY 轉 TWD
[4] TWD 轉 JPY
[5] EUR 轉 TWD
[6] USD 轉 JPY
[0] 自訂輸入幣別 (Custom Currency)
[L] 查詢所有支援幣別清單 (List All Currencies)
==============================================
請選擇 (1-6, 0=自訂, L=清單) [預設: 1]: 1
TWD Amount: 5000
USD Amount: 151.9452
```

### Custom Currency Input (Option 0)
```txt
請選擇 (1-6, 0=自訂, L=清單) [預設: 1]: 0
Source currency: EUR
Target currency: JPY
EUR Amount: 50
JPY Amount: 8866.8711
```
