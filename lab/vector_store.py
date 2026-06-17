"""A minimal, intentionally insecure in-memory vector store.

It mirrors the security-relevant behaviour of a default Chroma deployment:

- no access control
- no document provenance or integrity checks
- metadata stored and returned alongside content
- optional JSON persistence (like Chroma's persistent client)

The *absence* of these controls is the vulnerability surface the scenarios
exercise. See the README for the mapping to real-world misconfigurations.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field

from lab.embeddings import cosine, embed


@dataclass
class Document:
    id: str
    content: str
    metadata: dict = field(default_factory=dict)
    embedding: list = field(default_factory=list)


class VectorStore:
    def __init__(self) -> None:
        self._docs: list[Document] = []

    def add(self, doc_id: str, content: str, metadata: dict | None = None) -> None:
        # By design: no provenance check, no dedup, no auth, no integrity hash.
        self._docs.append(
            Document(id=doc_id, content=content, metadata=metadata or {},
                     embedding=embed(content))
        )

    def query(self, text: str, k: int = 4) -> list[Document]:
        q = embed(text)
        ranked = sorted(self._docs, key=lambda d: cosine(q, d.embedding), reverse=True)
        return ranked[:k]

    def count(self) -> int:
        return len(self._docs)

    def save(self, path: str) -> None:
        with open(path, "w") as fh:
            json.dump([asdict(d) for d in self._docs], fh)

    def load(self, path: str) -> None:
        with open(path) as fh:
            self._docs = [Document(**d) for d in json.load(fh)]
