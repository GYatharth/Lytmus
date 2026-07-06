# Lytmus

An AI research agent that searches, retrieves, and synthesizes answers — but unlike most RAG agents, it doesn't present every claim with equal confidence. Each claim in the final answer is scored and tagged based on how well it's actually supported by the retrieved evidence.

## The problem

Most research agents (and most RAG demos) treat every generated sentence as equally trustworthy, whether it's backed by three independent sources or a single ambiguous one. That's a trust problem: users can't tell a well-corroborated fact from a shaky extrapolation.

## The differentiator

Every stage of this pipeline still uses AI/ML — retrieval, synthesis, and
scoring are all neural-network-based. What it does **not** do is ask an
LLM to grade its own answer ("how confident are you, 1-100?") or decide
whether two sources agree. That specific pattern is known to be
unreliable — LLMs are poorly calibrated at self-rating their own
certainty, so a model can sound equally confident whether it's right
or wrong.

Instead, citation and verification are split into two separate stages:

1. **The LLM cites, during synthesis.** It writes the answer and attaches
   citation markers pointing to the retrieved source chunks it used —
   this is standard RAG behavior, no different from other agents.
2. **A deterministic layer checks the citation afterward**, using signals
   that don't depend on LLM judgment:
   - **Semantic entailment** — embedding similarity between the claim
     sentence and its cited source passage (a neural network, but not a
     generative opinion — just a similarity score)
   - **Source agreement count** — how many independent sources support
     the same claim (plain counting, no AI needed)
   - **Numeric contradiction detection** — extracted (metric, dataset,
     score) triples compared across papers, so "Paper A reports 91% on
     GLUE" vs. "Paper B reports a conflicting 84% baseline" gets flagged
     directly, not inferred by an LLM's opinion of "conflict"
   - **Recency weighting within topic clusters** — a 2025 paper claiming
     to beat a 2021 SOTA isn't a "contradiction," it's supersession;
     the scorer treats these differently

So the LLM's citation is treated as a claim to verify, not a fact to
trust — the verification step is what makes the confidence tags
trustworthy rather than just another LLM opinion wearing a percentage
sign.

## Why CS/ML research papers specifically

This is not a general web-search trust layer — the scoring signals above
(numeric contradiction, recency-aware supersession, citation structure)
only make sense for a corpus of research papers. A 2021 paper being
"outdated" by a 2025 one isn't a conflict the way two disagreeing news
articles are; a general search agent has no reason to model that
distinction, but a research-literature tool has to.

## Architecture

1. **Query planner** — decomposes the user's question into sub-questions
2. **Dual retrieval** — web search (Tavily API) + local corpus (FAISS vector index)
3. **Agent orchestrator** — routes tools, executes calls, merges results
4. **Synthesis engine** — LLM writes a cited answer from merged retrieval results
5. **Verification layer** — deterministic checks (entailment similarity, agreement count, numeric contradiction, recency weighting) score each cited claim
6. **Streamlit UI** — displays the answer with citations, confidence tags, and a citation graph

## Tech stack

Python · LangChain · Groq (fast inference for planning/orchestration) · Tavily API · FAISS · sentence-transformers · Streamlit

## Features

- Query decomposition + dual retrieval (live web + local arXiv corpus)
- LLM synthesis with citations, verified afterward by a deterministic layer (not LLM self-rating)
- Numeric contradiction detection — flags conflicting reported metrics across papers (e.g. differing benchmark scores), not just "sources disagree"
- Recency-aware supersession — distinguishes an outdated claim from a genuinely contradicted one
- Citation graph visualization — shows how cited papers relate, not just a flat source list
- Second-pass verification agent that critiques claims before scoring (v2)
- Clickable citations and per-claim feedback
- Public live demo (see link once deployed)

## Domain

Local corpus: computer science / ML research papers (arXiv). Keeps the
scope focused and plays to a CSE background — the story becomes
"a confidence-scored research agent for CS/ML literature," not a
generic ask-anything tool.

## Status

🚧 In active development, paced by milestones rather than a fixed deadline.
Full plan in `PLAN.md`.

## Why this exists

Built as a portfolio project demonstrating agentic tool orchestration, RAG, and a calibrated trust layer — the same score/explain separation used in [Calibr](https://github.com/) applied to open-ended research queries instead of resume scoring.
