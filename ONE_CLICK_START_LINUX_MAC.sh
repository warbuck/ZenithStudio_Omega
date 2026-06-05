#!/bin/bash
# ONE_CLICK_START_LINUX_MAC.sh
# ZenithStudio Omega v4.8.0 - Linux/macOS Launcher

echo ""
echo "============================================================"
echo "  ZenithStudio Omega v4.8.0 - Linux/macOS Setup"
echo "============================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.10+"
    exit 1
fi

echo "[1/5] Checking requirements..."
pip3 install -r requirements.txt > /dev/null 2>&1

echo "[2/5] Initializing directories..."
mkdir -p data/missions logs workspace

echo "[3/5] Running self-test..."
python3 ZenithStudio.py --self-test > /dev/null 2>&1

echo "[4/5] Starting backend..."
echo "Backend will start on http://127.0.0.1:5000"

echo "[5/5] Starting ZenithStudio Omega..."
echo ""

python3 ZenithStudio.py
