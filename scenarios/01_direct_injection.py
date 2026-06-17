"""Scenario 1 - Direct Prompt Injection via Document Content.

Runs fully offline (no API key). It seeds a clean knowledge base, asks a benign
question to show normal behaviour, then plants a single poisoned document and
asks the *same* question again. The agent follows the instruction hidden in the
retrieved document - with no access to the system prompt and no malicious user
input.

    python scenarios/01_direct_injection.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from attacks.payloads import DIRECT_INJECTION  # noqa: E402
from lab.rag_pipeline import VulnerableRAG  # noqa: E402
from lab.vector_store import VectorStore  # noqa: E402


def seed_clean(store: VectorStore) -> None:
    store.add("policy-balance",
              "To check an account balance, verify the customer's identity, "
              "then read the balance from the core banking API.",
              {"source": "ops-handbook", "category": "approved"})
    store.add("policy-export",
              "Data export requests must be approved by the data protection "
              "officer before any data leaves the system.",
              {"source": "compliance", "category": "approved"})


def banner(label: str) -> None:
    print("\n" + "=" * 70 + f"\n{label}\n" + "=" * 70)


def main() -> None:
    question = "How do I handle a data export request?"

    banner("BEFORE - clean knowledge base")
    store = VectorStore()
    seed_clean(store)
    rag = VulnerableRAG(store=store)
    resp = rag.ask(question)
    print("Q:", question)
    print("retrieved:", resp.retrieved_ids)
    print("A:", resp.answer)

    banner("ATTACK - plant one poisoned document")
    poison = DIRECT_INJECTION[0]
    store.add(poison["id"], poison["content"], poison["metadata"])
    print("planted doc id:", poison["id"])
    print("payload:", poison["content"].strip().splitlines()[0], "...")

    banner("AFTER - same question, poisoned knowledge base")
    resp = rag.ask(question)
    print("Q:", question)
    print("retrieved:", resp.retrieved_ids)
    print("A:", resp.answer)

    banner("RESULT")
    print("The retrieved document's instruction was followed. The agent never")
    print("saw a malicious *user* - the attack arrived through trusted content.")
    print("The fix is not a better prompt; it is isolating retrieved content")
    print("from instructions. See the guardrail in secure-enterprise-knowledge-hub.")


if __name__ == "__main__":
    main()
