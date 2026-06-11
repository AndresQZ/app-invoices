#!/bin/bash
echo "========================================"
echo " Starting Project Setup..."
echo "========================================"


echo "-> Creating virtual environment (.venv)..."
python -m venv .venv

echo "-> Activating environment..."
source .venv/bin/activate

echo "-> Installing dependencies from requirements.txt..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "========================================"
echo "done"
echo " Run 'source .venv/bin/activate' to activate your environment."
echo "========================================"