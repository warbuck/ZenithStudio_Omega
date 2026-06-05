"""AI Model Providers"""

import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

logger = logging.getLogger('ModelProvider')

class ModelProvider(ABC):
    """Abstract model provider"""
    
    @abstractmethod
    def query(self, prompt: str) -> str:
        pass

class LocalDeterministicProvider(ModelProvider):
    """Local deterministic fallback - always available"""
    
    def query(self, prompt: str) -> str:
        """Return deterministic response"""
        return "Local deterministic response. Model provider not configured."

class OllamaProvider(ModelProvider):
    """Ollama-compatible provider"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:11434"):
        self.base_url = base_url
        self.available = False
        self._check_availability()
    
    def _check_availability(self):
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            self.available = response.status_code == 200
        except:
            self.available = False
    
    def query(self, prompt: str) -> str:
        if not self.available:
            return LocalDeterministicProvider().query(prompt)
        return f"Ollama response to: {prompt[:50]}..."

class OpenAIProvider(ModelProvider):
    """OpenAI-compatible provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.available = bool(api_key)
    
    def query(self, prompt: str) -> str:
        if not self.available:
            return LocalDeterministicProvider().query(prompt)
        return f"OpenAI response to: {prompt[:50]}..."

class LlamaCppProvider(ModelProvider):
    """llama.cpp-compatible provider"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.available = False
    
    def query(self, prompt: str) -> str:
        if not self.available:
            return LocalDeterministicProvider().query(prompt)
        return f"llama.cpp response to: {prompt[:50]}..."

class ModelVault:
    """Manage available model providers"""
    
    def __init__(self):
        self.providers = {
            'local': LocalDeterministicProvider(),
            'ollama': OllamaProvider(),
            'openai': OpenAIProvider(),
            'llamacpp': LlamaCppProvider()
        }
        self.default_provider = 'local'
    
    def query(self, prompt: str, provider: Optional[str] = None) -> str:
        """Query a model provider"""
        provider_name = provider or self.default_provider
        provider_obj = self.providers.get(provider_name, self.providers['local'])
        return provider_obj.query(prompt)
