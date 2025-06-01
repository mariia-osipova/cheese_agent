#!/usr/bin/env bash
echo "→ DEBUG: Langflow will listen to $PORT"
export LANGFLOW_BACKEND_ONLY=1
langflow run --host 0.0.0.0 --port "$PORT"

