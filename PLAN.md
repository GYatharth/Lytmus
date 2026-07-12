# Build plan

Sequenced deliberately: core pipeline first, THEN retrieval upgrades,
THEN infra, THEN extra features, THEN production polish. Don't jump
ahead — Docker around a half-built system teaches you Docker, not
Lytmus, and you specifically want to understand every layer.

---

## PHASE A — Core pipeline (build this fully before anything else)

### Milestone 1 — Scaffolding
- [ ] Repo + folder structure
- [ ] Groq + Tavily API keys wired up, smoke test
- [ ] Domain: CS/ML research papers (arXiv) — corpus collected, FAISS index built

### Milestone 2 — Retrieval
- [ ] Query planner (decompose multi-part questions)
- [ ] Web search retrieval path (Tavily) working standalone
- [ ] Local corpus retrieval path (FAISS) working standalone

### Milestone 3 — Orchestration + core differentiator
- [ ] Agent orchestrator (LangChain tool-calling, merges both retrieval paths)
- [ ] Synthesis engine (LLM writes cited answer)
- [ ] Verification layer v1: semantic entailment + source agreement count
- [ ] Verification layer tuned on 15–20 hand-labeled test queries

### Milestone 4 — Research-specific trust features
- [ ] Numeric contradiction detection (metric/dataset/score triples)
- [ ] Recency-aware supersession
- [ ] Citation graph (Semantic Scholar API)
- [ ] Custom weighted confidence formula (explicit, e.g.
      `0.35*agreement + 0.25*entailment + 0.20*recency + 0.20*citation_quality`
      — tune weights against your hand-labeled set, don't guess-and-freeze)
- [ ] Confidence breakdown UI (show WHY 84%, not just the number)

### Milestone 5 — Verification agent (v2)
- [ ] Second-pass agent that critiques claims before scoring
- [ ] Compare scorer accuracy with vs. without the verification pass

### Milestone 6 — Ship the core product
- [ ] Streamlit UI — citations, confidence tags, verification breakdown
- [ ] Deploy publicly (Streamlit Community Cloud / HF Spaces)
- [ ] README polish, demo recording

**Do not move to Phase B until Phase A works end-to-end and you can
explain every piece of it out loud without looking at your own code.**

---

## PHASE B — Retrieval quality upgrades

- [ ] BM25 keyword search added alongside FAISS (hybrid retrieval)
- [ ] Reciprocal Rank Fusion to merge BM25 + embedding results
- [ ] Cross-encoder reranking on top-30 candidates → top 8-10 final
- [ ] Metadata filtering (year, venue, category)

---

## PHASE C — Backend + infra

- [ ] FastAPI backend (Streamlit becomes UI-only, calls FastAPI — stop
      using Streamlit as a backend)
- [ ] Redis caching layer for Groq/Tavily/Semantic Scholar/embedding calls
- [ ] PostgreSQL for paper metadata, query history (vectors stay in FAISS,
      structured data moves out of it)
- [ ] Pydantic schemas for all API request/response models
- [ ] Logging: latency per stage (retrieval, LLM, scoring), token usage

---

## PHASE D — Evaluation

- [ ] Custom eval script (precision/recall against your hand-labeled set —
      you already do this in Milestone 5, extend it)
- [ ] Ragas and/or DeepEval integrated for faithfulness / context precision /
      answer relevancy metrics
- [ ] Results written up in README with real numbers from your own test set

---

## PHASE E — Scaling / async

- [ ] Celery + Redis for background jobs (async indexing of new papers)
- [ ] Incremental FAISS indexing (embed only new papers, don't rebuild)
- [ ] Background worker: new paper arrives → download → chunk → embed → store

---

## PHASE F — Extra features (build in this order — earlier ones are
higher value for less effort; later ones are bigger lifts)

- [ ] Claim Verification Table (structured claim/evidence/status view)
- [ ] Citation graph polish (node size = citation count, color = year)
- [ ] Paper Comparison (method/dataset/accuracy/limitations side by side)
- [ ] Conflicting Opinion Detection UI (show WHY two papers disagree, not
      just that they do — different benchmark, different setup, etc.)
- [ ] Timeline View (research evolution over years for a topic)
- [ ] Research Gap Finder (common limitations / open challenges across a
      paper set)
- [ ] Conversation memory (follow-up questions referencing prior answer)
- [ ] Auto BibTeX/APA/IEEE export
- [ ] Novelty detection (what specifically changed between two similar papers)
- [ ] Automatic literature review generation
- [ ] Paper recommendations (related/survey/foundational papers)
- [ ] PDF highlighting (click claim → highlight source paragraph in PDF)
- [ ] Reading difficulty scoring
- [ ] Research trends dashboard (active topics, top authors, emerging keywords)

---

## PHASE G — Production polish

- [ ] Docker + Docker Compose (one-command deploy: FastAPI + Redis +
      Postgres + frontend)
- [ ] GitHub Actions CI/CD (lint, test, build on push)
- [ ] Pytest coverage (retrieval tests, verification tests, API tests)
- [ ] Monitoring dashboard (avg latency, cache hit %, avg confidence,
      cost estimation) — Prometheus + Grafana if you want to go further
- [ ] Security pass: input validation, rate limiting, secrets audit

---

## Domain: computer science / ML research (arXiv)
arXiv has a free, clean API (no scraping, no auth) — fastest path to a real corpus.
Categories to start with: cs.CL, cs.LG, cs.IR.

## Architecture target (end state)
Streamlit (UI only)
↓
FastAPI
↓
LangChain Agent (query planning + tool orchestration)
↓
Hybrid Retrieval (BM25 + FAISS) → Cross-Encoder Reranking
↓
Groq LLM (synthesis)
↓
Verification Engine
• source agreement
• semantic entailment
• numeric contradiction
• recency weighting
• weighted confidence formula
↓
Citation Graph
↓
Evaluation (custom + Ragas/DeepEval)
↓
Redis Cache · PostgreSQL · Celery Workers · Docker

## A note on scope

This is a large plan by design — the goal is deep, defensible understanding
of every layer, not just checking boxes. If any phase starts feeling like
copy-pasted code you can't explain, stop and go back to the Milestone 0
warm-up exercises for that concept before continuing. Breadth without
depth defeats the actual point of this project.