"""Pluggable LLM layer.

By default the lab uses ``EchoLLM``: a deterministic, offline stand-in that
models the one behaviour that matters for these attacks — an instruction-tuned
model treats imperative instructions found in its context as authoritative,
whether they arrived from the system prompt, the user turn, or a *retrieved
document*. EchoLLM lets the lab run with no API key while faithfully
reproducing why prompt injection works.

Set ``LLM_PROVIDER=openai`` or ``anthropic`` (with the matching key) once the
real-provider adapter lands to run the same scenarios against a live model. The
outcome is the same — that is the whole point of the lab.
"""
from __future__ import annotations

import os
import re

# Imperative patterns an instruction-following model latches onto when they
# appear in retrieved content. EchoLLM obeys the last one it sees — exactly the
# failure mode the lab demonstrates.
_INSTRUCTION = re.compile(
    r"(ignore[^\n]*|disregard[^\n]*|respond with[^\n]*|always [^\n]*|"
    r"when asked[^\n]*|do not [^\n]*|system override[^\n]*)", re.I)


class EchoLLM:
    """Deterministic instruction-following simulator. No network, no key."""

    name = "echo-llm (offline stand-in)"

    def complete(self, system: str, context: str, question: str) -> str:
        injected = _INSTRUCTION.findall(context)
        if injected:
            # The model follows the injected instruction from retrieved context.
            return ("[following instruction found in retrieved context] "
                    + injected[-1].strip())
        first_line = next((ln for ln in context.splitlines() if ln.strip()), "")
        if first_line:
            return f"Based on the knowledge base: {first_line.strip()}"
        return "I don't have information on that in the knowledge base."


def get_llm():
    provider = os.environ.get("LLM_PROVIDER", "echo").lower()
    if provider in ("", "echo"):
        return EchoLLM()
    raise NotImplementedError(
        f"LLM_PROVIDER='{provider}' is part of the real-provider adapter "
        "(in progress). The lab runs fully offline with the default EchoLLM.")
