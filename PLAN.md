# Build plan

# Build plan

No hard deadline — paced by milestones completed, not calendar weeks.
Move to the next milestone only once the current one actually works end-to-end.

## Milestone 1 — Scaffolding
- [x] Repo + folder structure
- [ ] Tavily + Groq API keys wired up, smoke test
- [ ] Domain chosen, local corpus collected and FAISS index built

## Milestone 2 — Retrieval
- [ ] Query planner (decompose multi-part questions)
- [ ] Web search retrieval path working standalone
- [ ] Local corpus retrieval path working standalone

## Milestone 3 — Orchestration + core differentiator
- [ ] Agent orchestrator (tool routing, merges both retrieval paths)
- [ ] Synthesis engine (LLM writes cited answer from merged retrieval results)
- [ ] Verification layer v1: semantic entailment + source agreement count
- [ ] Verification layer tuned on 15–20 test queries

## Milestone 4 — Research-specific trust features
- [ ] Numeric contradiction detection (extract metric/dataset/score triples,
      flag conflicting reported numbers across papers)
- [ ] Recency-aware supersession (distinguish "outdated" from "contradicted")
- [ ] Citation graph (relationships between cited papers — needs Semantic
      Scholar API or similar, since arXiv's own API has no citation links)
- [ ] Clickable citations (click a claim, highlight the source passage)
- [ ] Feedback loop (thumbs up/down per claim, stored for future recalibration)

## Milestone 5 — Verification agent (v2 differentiator)
- [ ] Second-pass agent that critiques the draft's claims against sources
      before the confidence scorer runs (lightweight "debate" pattern)
- [ ] Compare scorer accuracy with vs. without the verification pass on the
      test set — this comparison itself is a strong resume-worthy result

## Milestone 6 — Polish + ship
- [ ] Streamlit UI — citations + confidence tags, clean layout
- [ ] Deploy publicly (Streamlit Community Cloud / HF Spaces)
- [ ] README polish, demo recording, final push

## Domain: computer science / ML research (arXiv)
Chosen over finance/health to match CSE background and because arXiv has
a free, clean API (no scraping, no auth) — fastest path to a real corpus.
Practical starting point: pull abstracts + full text for a few hundred
papers from 2-3 related arXiv categories (e.g. cs.CL, cs.LG, cs.IR) via
the arXiv API (http://export.arxiv.org/api/query), chunk, embed with
sentence-transformers, and build the FAISS index from that set.
