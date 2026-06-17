"""Seed the lab vector store with clean, benign documents.

    python setup/init_knowledge_base.py

Writes a persisted store to ``$LAB_DB_PATH`` (default: lab_kb.json) that the
scenarios can load. Each scenario can also build its own clean state in-memory,
so running this first is optional.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab.vector_store import VectorStore  # noqa: E402

CLEAN_DOCS = [
    ("policy-balance",
     "To check an account balance, verify the customer's identity with two "
     "factors, then read the balance from the core banking API.",
     {"source": "ops-handbook", "category": "approved"}),
    ("policy-transfer",
     "Account transfers above $10,000 require secondary approval from a "
     "supervisor before processing.",
     {"source": "ops-handbook", "category": "approved"}),
    ("policy-export",
     "Data export requests must be logged and approved by the data protection "
     "officer before any data leaves the system.",
     {"source": "compliance", "category": "approved"}),
    ("faq-hours",
     "Customer support operates 9am to 5pm Eastern, Monday through Friday.",
     {"source": "faq", "category": "public"}),
]

DB_PATH = os.environ.get("LAB_DB_PATH", "lab_kb.json")


def build() -> VectorStore:
    store = VectorStore()
    for doc_id, content, meta in CLEAN_DOCS:
        store.add(doc_id, content, meta)
    store.save(DB_PATH)
    print(f"seeded {store.count()} clean documents -> {DB_PATH}")
    return store


if __name__ == "__main__":
    build()
