"""agentic-rag-security-lab — minimal, dependency-free vulnerable RAG core.

The core lab runs on the Python standard library alone so the attack scenarios
are reproducible offline, with no API key and no model downloads. The
LangChain/Chroma adapter and real-LLM providers are documented as in progress
in the README; they swap these modules out without changing the scenarios.
"""
