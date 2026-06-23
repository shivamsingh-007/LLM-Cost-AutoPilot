from __future__ import annotations

import time
import os
from dataclasses import dataclass, asdict, field
from typing import Dict, Optional

from core.models_config import ModelConfig, Provider


@dataclass
class Response:
    output: str
    tokens: Dict[str, int] = field(default_factory=lambda: {"input": 0, "output": 0})
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    model_id: str = ""
    provider: str = ""
    success: bool = True
    error_message: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class UnifiedLLMInterface:
    def __init__(self) -> None:
        self._openai_key = os.getenv("OPENAI_API_KEY", "")
        self._anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self._ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self._openai_client = None
        self._anthropic_client = None
        self._ollama_client = None

    def _get_openai(self):
        if self._openai_client is None:
            try:
                from openai import AsyncOpenAI as _AsyncOpenAI
                self._openai_client = _AsyncOpenAI(api_key=self._openai_key)
            except ImportError:
                return None
        return self._openai_client

    def _get_anthropic(self):
        if self._anthropic_client is None:
            try:
                from anthropic import AsyncAnthropic as _AsyncAnthropic
                self._anthropic_client = _AsyncAnthropic(api_key=self._anthropic_key)
            except ImportError:
                return None
        return self._anthropic_client

    def _get_ollama(self):
        if self._ollama_client is None:
            try:
                import ollama as _ollama
                self._ollama_client = _ollama.AsyncClient(host=self._ollama_host)
            except ImportError:
                return None
        return self._ollama_client

    async def send_request(
        self,
        prompt: str,
        model_config: ModelConfig,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Response:
        start = time.time()
        try:
            if model_config.provider == Provider.OPENAI:
                output, tokens = await self._call_openai(prompt, model_config, system_prompt, temperature, max_tokens)
            elif model_config.provider == Provider.ANTHROPIC:
                output, tokens = await self._call_anthropic(prompt, model_config, system_prompt, temperature, max_tokens)
            elif model_config.provider == Provider.OLLAMA:
                output, tokens = await self._call_ollama(prompt, model_config, system_prompt, temperature, max_tokens)
            else:
                raise ValueError(f"Unknown provider: {model_config.provider}")

            elapsed_ms = (time.time() - start) * 1000
            cost = model_config.estimate_cost(tokens["input"], tokens["output"])
            return Response(
                output=output,
                tokens=tokens,
                latency_ms=elapsed_ms,
                cost_usd=cost,
                model_id=model_config.model_id,
                provider=model_config.provider.value,
            )
        except Exception as e:
            elapsed_ms = (time.time() - start) * 1000
            return Response(
                output="",
                latency_ms=elapsed_ms,
                model_id=model_config.model_id,
                provider=model_config.provider.value,
                success=False,
                error_message=str(e),
            )

    async def _call_openai(
        self,
        prompt: str,
        model_config: ModelConfig,
        system_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> tuple[str, Dict[str, int]]:
        client = self._get_openai()
        if client is None:
            raise RuntimeError("OpenAI client not available. Install openai SDK.")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=model_config.model_id,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        choice = response.choices[0]
        output = choice.message.content or ""
        usage = response.usage
        tokens: Dict[str, int] = {}
        if usage:
            tokens["input"] = usage.prompt_tokens
            tokens["output"] = usage.completion_tokens
        return output, tokens

    async def _call_anthropic(
        self,
        prompt: str,
        model_config: ModelConfig,
        system_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> tuple[str, Dict[str, int]]:
        client = self._get_anthropic()
        if client is None:
            raise RuntimeError("Anthropic client not available. Install anthropic SDK.")

        kwargs: Dict = {
            "model": model_config.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = await client.messages.create(**kwargs)

        tokens: Dict[str, int] = {}
        if hasattr(response, "usage") and response.usage:
            tokens["input"] = getattr(response.usage, "input_tokens", 0)
            tokens["output"] = getattr(response.usage, "output_tokens", 0)

        content_blocks = response.content
        output = ""
        if content_blocks:
            for block in content_blocks:
                if hasattr(block, "text"):
                    output += block.text
        return output, tokens

    async def _call_ollama(
        self,
        prompt: str,
        model_config: ModelConfig,
        system_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> tuple[str, Dict[str, int]]:
        client = self._get_ollama()
        if client is None:
            raise RuntimeError("Ollama client not available. Install ollama SDK.")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat(
            model=model_config.model_id,
            messages=messages,
            options={
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        )

        output = response.get("message", {}).get("content", "")
        # ponytail: word-count heuristic, swap to tiktoken if accuracy matters
        input_tokens_est = max(1, int(len(prompt.split()) * 1.3))
        output_tokens_est = max(1, int(len(output.split()) * 1.3))

        tokens: Dict[str, int] = {
            "input": input_tokens_est,
            "output": output_tokens_est,
        }
        return output, tokens
