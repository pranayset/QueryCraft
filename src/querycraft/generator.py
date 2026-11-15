"""Public generation entry point backed by the lazy Gemma 3 adapter."""
from functools import lru_cache

from .model import GemmaCypherGenerator


@lru_cache(maxsize=1)
def _generator() -> GemmaCypherGenerator:
    return GemmaCypherGenerator()


def generate_cypher(question: str) -> str:
    """Generate one Cypher query using the configured private Gemma LoRA adapter."""
    return _generator().generate(question)
