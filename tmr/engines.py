"""
UTCS-MI: AQUART-TMR-ENGINES-engine_adapters-v1.0
Engine Adapters for OpenAI, Anthropic, Google with Provider Isolation
"""

import asyncio
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .core import PromptSpec, ResponseSpec, content_hash


class EngineAdapter(ABC):
    """Abstract base class for engine adapters"""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.total_requests = 0
        self.total_cost = 0.0
        self.last_health_check = 0.0

    @abstractmethod
    async def generate(self, prompt_spec: PromptSpec) -> ResponseSpec:
        """Generate response for the given prompt"""
        pass

    def health_check(self) -> bool:
        """Basic health check - override for actual implementation"""
        self.last_health_check = time.time()
        return True

    def _calculate_cost(self, tokens_in: int, tokens_out: int) -> float:
        """Calculate cost based on token usage"""
        # Mock pricing - replace with actual vendor pricing
        input_cost_per_token = 0.00001
        output_cost_per_token = 0.00003
        return (tokens_in * input_cost_per_token) + (tokens_out * output_cost_per_token)

    def _apply_safety_filters(self, content: str) -> str:
        """Apply safety filters: PII scrub, jailbreak detection"""
        # Mock implementation - in production would use actual filters
        
        # Basic PII patterns (emails, phone numbers)
        import re
        
        # Remove email addresses
        content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', content)
        
        # Remove phone numbers
        content = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE]', content)
        content = re.sub(r'\b\(\d{3}\)\s?\d{3}-\d{4}\b', '[PHONE]', content)
        
        # Basic jailbreak detection
        jailbreak_patterns = [
            "ignore previous instructions",
            "forget everything above", 
            "act as if you're",
            "pretend to be",
            "roleplay as"
        ]
        
        content_lower = content.lower()
        for pattern in jailbreak_patterns:
            if pattern in content_lower:
                raise ValueError(f"Potential jailbreak attempt detected: {pattern}")
        
        return content


class OpenAIAdapter(EngineAdapter):
    """OpenAI GPT-5 Thinking adapter"""
    
    def __init__(self, name: str = "engine_a"):
        super().__init__(name, {
            "model": "gpt-5-thinking",
            "vendor": "openai",
            "api_endpoint": "https://api.openai.com/v1/chat/completions"
        })

    async def generate(self, prompt_spec: PromptSpec) -> ResponseSpec:
        """Generate response using OpenAI API (mocked)"""
        start_time = time.time()
        
        # Mock API call - in production would use actual OpenAI SDK
        await asyncio.sleep(0.1)  # Simulate API latency
        
        # Extract controls
        temperature = prompt_spec.controls.get("temperature", 0.2)
        max_tokens = prompt_spec.controls.get("max_tokens", 1000)
        
        # Mock response generation
        mock_content = {
            "response": f"OpenAI response to: {prompt_spec.template[:50]}...",
            "model": self.config["model"],
            "reasoning": "Mock reasoning chain for deterministic output",
            "confidence": 0.95
        }
        
        # Apply safety filters
        filtered_content = self._apply_safety_filters(str(mock_content))
        mock_content["filtered"] = True
        
        tokens_in = len(prompt_spec.template.split()) + sum(len(str(v).split()) for v in prompt_spec.inputs.values())
        tokens_out = len(filtered_content.split())
        
        latency_ms = int((time.time() - start_time) * 1000)
        cost = self._calculate_cost(tokens_in, tokens_out)
        
        self.total_requests += 1
        self.total_cost += cost
        
        return ResponseSpec(
            engine=self.name,
            latency_ms=latency_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost=cost,
            content=mock_content,
            content_hash=content_hash(mock_content),
            timestamp=time.time()
        )

    def health_check(self) -> bool:
        """Health check for OpenAI service"""
        try:
            # Mock health check - in production would ping actual API
            self.last_health_check = time.time()
            return True
        except Exception:
            return False


class AnthropicAdapter(EngineAdapter):
    """Anthropic Claude-Next adapter"""
    
    def __init__(self, name: str = "engine_b"):
        super().__init__(name, {
            "model": "claude-next",
            "vendor": "anthropic", 
            "api_endpoint": "https://api.anthropic.com/v1/messages"
        })

    async def generate(self, prompt_spec: PromptSpec) -> ResponseSpec:
        """Generate response using Anthropic API (mocked)"""
        start_time = time.time()
        
        # Mock API call
        await asyncio.sleep(0.15)  # Simulate slightly different latency
        
        temperature = prompt_spec.controls.get("temperature", 0.2)
        max_tokens = prompt_spec.controls.get("max_tokens", 1000)
        
        # Mock response with different structure
        mock_content = {
            "response": f"Anthropic analysis of: {prompt_spec.template[:50]}...",
            "model": self.config["model"],
            "analysis": "Mock analytical response with safety considerations",
            "certainty": 0.92
        }
        
        filtered_content = self._apply_safety_filters(str(mock_content))
        mock_content["filtered"] = True
        
        tokens_in = len(prompt_spec.template.split()) + sum(len(str(v).split()) for v in prompt_spec.inputs.values())
        tokens_out = len(filtered_content.split())
        
        latency_ms = int((time.time() - start_time) * 1000)
        cost = self._calculate_cost(tokens_in, tokens_out) * 1.1  # Slightly higher cost
        
        self.total_requests += 1
        self.total_cost += cost
        
        return ResponseSpec(
            engine=self.name,
            latency_ms=latency_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost=cost,
            content=mock_content,
            content_hash=content_hash(mock_content),
            timestamp=time.time()
        )

    def health_check(self) -> bool:
        """Health check for Anthropic service"""
        try:
            self.last_health_check = time.time()
            return True
        except Exception:
            return False


class GoogleAdapter(EngineAdapter):
    """Google Gemini Ultra adapter"""
    
    def __init__(self, name: str = "engine_c"):
        super().__init__(name, {
            "model": "gemini-ultra",
            "vendor": "google",
            "api_endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-ultra:generateContent"
        })

    async def generate(self, prompt_spec: PromptSpec) -> ResponseSpec:
        """Generate response using Google API (mocked)"""
        start_time = time.time()
        
        # Mock API call
        await asyncio.sleep(0.12)  # Different latency profile
        
        temperature = prompt_spec.controls.get("temperature", 0.2)
        max_tokens = prompt_spec.controls.get("max_tokens", 1000)
        
        # Mock response with Google's format
        mock_content = {
            "response": f"Google Gemini evaluation of: {prompt_spec.template[:50]}...",
            "model": self.config["model"],
            "candidates": [
                {
                    "content": "Mock structured response",
                    "safety_ratings": {"harassment": "NEGLIGIBLE", "hate_speech": "NEGLIGIBLE"}
                }
            ],
            "accuracy": 0.89
        }
        
        filtered_content = self._apply_safety_filters(str(mock_content))
        mock_content["filtered"] = True
        
        tokens_in = len(prompt_spec.template.split()) + sum(len(str(v).split()) for v in prompt_spec.inputs.values())
        tokens_out = len(filtered_content.split())
        
        latency_ms = int((time.time() - start_time) * 1000)
        cost = self._calculate_cost(tokens_in, tokens_out) * 0.8  # Slightly lower cost
        
        self.total_requests += 1
        self.total_cost += cost
        
        return ResponseSpec(
            engine=self.name,
            latency_ms=latency_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost=cost,
            content=mock_content,
            content_hash=content_hash(mock_content),
            timestamp=time.time()
        )

    def health_check(self) -> bool:
        """Health check for Google service"""
        try:
            self.last_health_check = time.time()
            return True
        except Exception:
            return False


class LocalLLMAdapter(EngineAdapter):
    """Local lightweight model for tiebreaking"""
    
    def __init__(self, name: str = "engine_d_tiebreaker"):
        super().__init__(name, {
            "model": "local-llm-7b",
            "vendor": "local",
            "api_endpoint": "http://localhost:8000/generate"
        })

    async def generate(self, prompt_spec: PromptSpec) -> ResponseSpec:
        """Generate response using local model (mocked)"""
        start_time = time.time()
        
        # Faster local inference
        await asyncio.sleep(0.05)
        
        # Simpler response for tiebreaking
        mock_content = {
            "response": f"Local tiebreaker decision for: {prompt_spec.template[:30]}",
            "model": self.config["model"],
            "decision": "tiebreaker_choice_a",  # Deterministic tiebreaking
            "confidence": 0.75
        }
        
        tokens_in = len(prompt_spec.template.split())
        tokens_out = 20  # Short tiebreaker response
        
        latency_ms = int((time.time() - start_time) * 1000)
        cost = 0.0  # No cost for local model
        
        return ResponseSpec(
            engine=self.name,
            latency_ms=latency_ms,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost=cost,
            content=mock_content,
            content_hash=content_hash(mock_content),
            timestamp=time.time()
        )