#!/usr/bin/env bash

echo "→ DEBUG: which python3: $(which python3)"
echo "→ DEBUG: python3 version: $(python3 --version)"
echo "→ DEBUG: pip list (first 20):"
python3 -m pip list | head -n 20

echo "→ DEBUG: Langflow will listen to port $PORT"
export LANGFLOW_BACKEND_ONLY=1
python3 -m langflow run --host 0.0.0.0 --port "$PORT"
