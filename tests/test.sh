#!/bin/bash


export SERVICE_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $SERVICE_ROOT_PATH


echo "Testing CREATE"
python test_create.py

echo ""
echo "Testing READ"
python test_read.py
