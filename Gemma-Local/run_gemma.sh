#!/bin/bash
# Script to download and run Gemma 4 12B IT on Mac (Metal optimized)
# Dedicated folder version: /Users/emilioranucoli/Desktop/Oficina_Ranuk/Gemma-Local

set -e

# Setup directories relative to the script location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODEL_DIR="$SCRIPT_DIR/models"
MODEL_NAME="gemma-4-12B-it-Q4_K_M.gguf"
MODEL_PATH="$MODEL_DIR/$MODEL_NAME"
HF_REPO="bartowski/gemma-4-12B-it-GGUF"

# Configurable options via environment variables (with defaults)
PORT="${PORT:-8085}"
HOST="${HOST:-127.0.0.1}"
CTX_SIZE="${CTX_SIZE:-8192}"

echo "============================================================"
echo "Gemma 4 12B IT runner for macOS (llama.cpp + Metal)"
echo "============================================================"
echo "Gemma directory: $SCRIPT_DIR"
echo "Models directory: $MODEL_DIR"
echo "Model target: $MODEL_PATH"
echo "Port: $PORT"
echo "Host: $HOST"
echo "Context size: $CTX_SIZE"
echo "============================================================"

# Ensure models directory exists
mkdir -p "$MODEL_DIR"

# Download model if it doesn't exist
if [ ! -f "$MODEL_PATH" ]; then
    echo "Model file not found at: $MODEL_PATH"
    echo "Downloading Gemma 4 12B IT (Q4_K_M) from Hugging Face repository '$HF_REPO'..."
    
    # Check if hf is installed
    if ! command -v hf &> /dev/null; then
        echo "Error: hf (huggingface CLI) is not installed or not in PATH."
        echo "Please install it via brew: brew install hf"
        exit 1
    fi

    echo "Using HF CLI: hf"
    
    # Execute the download command
    hf download "$HF_REPO" "$MODEL_NAME" --local-dir "$MODEL_DIR"
    
    echo "Download completed successfully!"
else
    echo "Model file found at: $MODEL_PATH"
fi

# Locate llama-server
LLAMA_SERVER=""
if command -v llama-server &> /dev/null; then
    LLAMA_SERVER="llama-server"
elif [ -x "/opt/homebrew/bin/llama-server" ]; then
    LLAMA_SERVER="/opt/homebrew/bin/llama-server"
else
    echo "Error: llama-server is not found. Please install it using Homebrew: brew install llama.cpp"
    exit 1
fi

echo "Using llama-server path: $LLAMA_SERVER"
echo "Starting llama-server with Apple Metal acceleration & optimized 32K context..."
echo "Press Ctrl+C to stop the server."
echo "------------------------------------------------------------"

# Launch the server with optimal memory and context flags
# -ngl 99: offload all layers to GPU (Metal)
# -fa on: enable flash attention for memory efficiency
# -ctk q8_0 -ctv q8_0: quantize KV cache to save RAM/VRAM
# --jinja: plantilla de chat (necesario). --reasoning off: sin thinking verboso (reply no vacío + 2x
# más rápido en M4). mmap por DEFAULT (no --no-mmap): pesos paginan del GGUF, no ensucian swap en 16GB.
# threads 8 (deja 2 cores al SO), parallel 1 (un solo KV cache), cont-batching barato.
exec "$LLAMA_SERVER" \
    -m "$MODEL_PATH" \
    -c "$CTX_SIZE" \
    -ngl 99 \
    -fa on \
    -ctk q8_0 \
    -ctv q8_0 \
    --jinja \
    --reasoning off \
    --threads 8 \
    --parallel 1 \
    --cont-batching \
    --host "$HOST" \
    --port "$PORT"
