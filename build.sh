#!/bin/bash
uv run python \
    -m nuitka \
    --mode=onefile \
    --output-dir=dist \
    main.py
