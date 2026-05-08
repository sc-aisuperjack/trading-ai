#!/usr/bin/env bash
set -e
echo "Starting simple Cognizant Trading Assistant..."
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ ! -f .env ]; then cp .env.example .env; fi
streamlit run app.py
