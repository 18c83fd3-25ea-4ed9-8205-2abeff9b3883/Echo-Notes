import requests
from .config import LM_URL, LLM_MODEL

def query_llm(prompt: str, system_message: str, max_tokens=2000) -> str:
    """Generic LLM query handler"""
    payload = {
        "model": LLM_MODEL,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(LM_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"LLM request failed: {str(e)}")