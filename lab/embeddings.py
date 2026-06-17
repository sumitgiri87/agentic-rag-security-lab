"""Deterministic, dependency-free text embeddings.

This is intentionally NOT a production embedding model. It is a signed hashing
bag-of-words embedding: deterministic, offline, no downloads. It is sufficient
to demonstrate similarity-ranked retrieval and the attack classes in this repo.
The LangChain/Chroma adapter (in progress) replaces it with real sentence
embeddings; the scenarios are unchanged.
"""
from __future__ import annotations

import hashlib
import math
import re

DIM = 256
_TOKEN = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def embed(text: str) -> list[float]:
    """Map text to a unit-length DIM-dimensional vector, deterministically."""
    vec = [0.0] * DIM
    for tok in _tokens(text):
        h = int(hashlib.md5(tok.encode()).hexdigest(), 16)
        idx = h % DIM
        sign = 1.0 if (h >> 8) & 1 else -1.0
        vec[idx] += sign
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))
