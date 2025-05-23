# Local LLM Integration with Phi-2

Echo Notes now supports local LLM inference using the Phi-2 model, which can significantly improve privacy and reduce dependency on external API services.

## Overview

The integration allows Echo Notes to:
- Run LLM inference locally using the Phi-2 model
- Automatically fall back to the external API if the local model is unavailable
- Configure whether to use the local model or always use the external API

## Requirements

- llama-cpp-python package (installed via pip)
- Phi-2 model in GGUF format (specifically phi-2.Q4_K_M.gguf)
- Approximately 2GB of disk space for the model file

## Installation

The Phi-2 model is now automatically downloaded during the Echo Notes installation process. No manual steps are required to set up the local LLM functionality.

### Automatic Installation

When you install Echo Notes using the provided installer:

1. The llama-cpp-python package is automatically installed (with OpenBLAS support when possible)
2. The Phi-2 model is automatically downloaded from Hugging Face during installation
3. The local model is enabled by default in the configuration

### Manual Installation (if needed)

If you need to manually install or reinstall the components:

1. Install the llama-cpp-python package:
   ```bash
   pip install llama-cpp-python
   ```
   
   For better performance with OpenBLAS:
   ```bash
   CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
   ```

2. Download the Phi-2 model:
   ```bash
   mkdir -p echo_notes/models
   wget -P echo_notes/models https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf
   ```

## Configuration

The local LLM integration can be configured in `echo_notes/shared/config.py`:

```python
# Set to True to use local model with fallback to API
# Set to False to always use the external API
USE_LOCAL_MODEL = True
```

## How It Works

1. When `query_llm()` is called, the system first checks if local inference is enabled
2. If enabled, it attempts to initialize the Phi-2 model (if not already loaded)
3. If the model is successfully loaded, it runs inference locally
4. If any issues occur (model not found, initialization error, inference error), it automatically falls back to the external API
5. The fallback mechanism ensures that Echo Notes continues to function even if the local model is unavailable

## Testing

You can test the local LLM integration using the provided test script:

```bash
python test_phi2.py
```

## Troubleshooting

If you encounter issues with the local model:

1. Ensure the model file exists at `echo_notes/models/phi-2.Q4_K_M.gguf`
2. Check that llama-cpp-python is properly installed
3. If you're experiencing performance issues, try installing llama-cpp-python with OpenBLAS support
4. Set `USE_LOCAL_MODEL = False` in config.py to temporarily disable local inference