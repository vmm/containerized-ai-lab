#!/usr/bin/env python3
"""
Script to download models from Ollama.
Usage: python download.py [model_name]

If model_name is not provided, it will download the default model specified in the .env file.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default model
DEFAULT_MODEL = os.getenv("MODEL_NAME", "llama2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def download_model(model_name):
    """Download a model from Ollama."""
    print(f"Downloading model: {model_name}...")
    
    try:
        # Call Ollama API to pull the model
        response = requests.post(
            f"{OLLAMA_HOST}/api/pull",
            json={"name": model_name}
        )
        
        if response.status_code == 200:
            print(f"Successfully downloaded model: {model_name}")
            return True
        else:
            print(f"Error downloading model: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def list_models():
    """List available models from Ollama."""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("\nAvailable models:")
            for model in models:
                print(f"- {model['name']}")
        else:
            print(f"Error listing models: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Get model name from command line argument or use default
    model_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
    
    success = download_model(model_name)
    
    if success:
        list_models()
    
    sys.exit(0 if success else 1)