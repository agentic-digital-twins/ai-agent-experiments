#!/usr/bin/env bash
set -e

MODEL_DIR="../../model"
MODEL_FILE="phi-2-q4_K_M.gguf"
MODEL_PATH="${MODEL_DIR}/${MODEL_FILE}"

URL="https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf"

mkdir -p "${MODEL_DIR}"

if [ -f "${MODEL_PATH}" ]; then
  echo "Model already exists at ${MODEL_PATH}"
  exit 0
fi

echo "Downloading Phi-2 Q4_K_M GGUF model..."
echo "From: ${URL}"
echo "To:   ${MODEL_PATH}"

curl -L "${URL}" -o "${MODEL_PATH}"

echo "Download complete."
