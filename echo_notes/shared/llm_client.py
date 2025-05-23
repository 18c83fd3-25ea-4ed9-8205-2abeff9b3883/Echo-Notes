import os
import requests
from pathlib import Path
from .config import LM_URL, LLM_MODEL

# Check if config.py has USE_LOCAL_MODEL, otherwise default to True
try:
    from .config import USE_LOCAL_MODEL
except ImportError:
    # Default to using local model if not defined in config
    USE_LOCAL_MODEL = True

# Initialize the model once as a global variable
MODEL_PATH = Path(__file__).parent.parent / "models" / "phi-2.Q4_K_M.gguf"
llm = None

def initialize_model():
    """Initialize the local Phi-2 model if not already done"""
    global llm
    if llm is None and MODEL_PATH.exists():
        try:
            from llama_cpp import Llama
            llm = Llama(
                model_path=str(MODEL_PATH),
                n_ctx=2048,
                n_threads=4,
                verbose=False
            )
            return True
        except Exception as e:
            print(f"Failed to initialize local model: {e}")
            return False
    return llm is not None

def query_llm(prompt: str, system_message: str, max_tokens=2000) -> str:
    """Generic LLM query handler with fallback to external API"""
    global llm
    
    # Try to use local model first if enabled
    if USE_LOCAL_MODEL:
        if initialize_model():
            try:
                # Combine system message and prompt to match the format expected by Phi-2
                combined_prompt = f"{system_message}\n\n{prompt}"
                
                output = llm(combined_prompt, max_tokens=max_tokens, temperature=0.7)
                return output["choices"][0]["text"].strip()
            except Exception as e:
                print(f"Local model error: {e}. Falling back to API.")
    
    # Fallback to external API
    try:
        payload = {
            "model": LLM_MODEL,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(LM_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"LLM request failed: {str(e)}")