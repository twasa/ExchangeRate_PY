#!/bin/bash
uv run pyinstaller -F --add-data currency_code.json:currency_code.json main.py
