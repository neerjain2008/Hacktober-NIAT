import json
import re
from typing import List, Optional, Tuple, Dict, Any
import httpx
from app.config import settings


class OllamaClient:
    def __init__(self, base_url: str = settings.OLLAMA_BASE_URL):
        self.base_url = base_url.rstrip("/")

    async def get_available_models(self) -> List[str]:
        """Fetch list of models currently pulled in the local Ollama instance."""
        try:
            async with httpx.AsyncClient(timeout=settings.OLLAMA_TAGS_TIMEOUT_SECONDS) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    data = res.json()
                    return [m.get("name", "") for m in data.get("models", []) if m.get("name")]
        except Exception:
            pass
        return []

    async def check_health(self) -> Dict[str, Any]:
        """Check if local Ollama daemon is reachable and return model metadata."""
        models = await self.get_available_models()
        is_online = len(models) > 0 or False
        # Also test base endpoint if models is empty
        if not is_online:
            try:
                async with httpx.AsyncClient(timeout=1.0) as client:
                    res = await client.get(self.base_url)
                    is_online = res.status_code == 200
            except Exception:
                is_online = False

        return {
            "ollama_online": is_online,
            "base_url": self.base_url,
            "models_available": models,
            "default_model": settings.DEFAULT_MODEL,
        }

    async def chat(
        self,
        prompt: str,
        preferred_model: Optional[str] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Query local Ollama for structured JSON completion.
        Returns (parsed_json_dict, model_name_used) or (None, None).
        """
        available = await self.get_available_models()
        if not available:
            return None, None

        # Choose model: exact/prefix match preferred -> gemma -> first available
        target_model = None
        if preferred_model:
            target_model = next((m for m in available if m.startswith(preferred_model)), None)
        if not target_model:
            target_model = next((m for m in available if "gemma" in m.lower()), available[0])

        payload = {
            "model": target_model,
            "messages": [{"role": "user", "content": prompt}],
            "format": "json",
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT_SECONDS) as client:
                res = await client.post(f"{self.base_url}/api/chat", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    content = data.get("message", {}).get("content", "")
                    parsed = self._extract_json(content)
                    if parsed:
                        return parsed, f"{target_model} (Local Ollama)"
        except Exception:
            pass

        return None, None

    @staticmethod
    def _extract_json(raw_text: str) -> Optional[Dict[str, Any]]:
        """Safely parse JSON from LLM output, extracting from markdown codeblocks if necessary."""
        if not raw_text:
            return None
        trimmed = raw_text.strip()
        code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", trimmed, re.IGNORECASE)
        to_parse = code_block_match.group(1).strip() if code_block_match else trimmed

        try:
            return json.loads(to_parse)
        except Exception:
            obj_match = re.search(r"\{[\s\S]*\}", to_parse)
            if obj_match:
                try:
                    return json.loads(obj_match.group(0))
                except Exception:
                    pass
        return None


ollama_client = OllamaClient()
