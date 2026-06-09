#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python -m pytest tests/test_alpha_contract.py -v
python -m uvicorn inspilot_cloud_baby.main:app --host 127.0.0.1 --port 8000
