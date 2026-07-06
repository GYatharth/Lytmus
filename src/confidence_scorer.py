"""
Confidence scorer / verification layer: the core differentiator of this project.

Synthesis (the LLM) writes citations during answer generation — that part is
standard RAG. This module treats each citation as a claim to VERIFY, not a
fact to trust, using signals that don't depend on asking an LLM to judge
itself:

- source_agreement: how many independent sources support the claim (counting)
- semantic_entailment: sentence-transformers similarity between claim and
  cited source passage
- numeric_contradiction: extracted (metric, dataset, score) triples compared
  across papers, so conflicting reported numbers are flagged directly
  instead of inferred from an LLM's opinion of "agree/disagree"
- recency_supersession: a later paper claiming to beat an earlier result is
  treated as superseding it, not contradicting it — these are scored
  differently

Each claim is bucketed into high / moderate / low confidence, plus an
optional "outdated" tag when recency_supersession applies.
"""


def score_claim(claim: str, supporting_chunks: list[dict]) -> dict:
    """
    Returns: {
        "tier": "high" | "moderate" | "low",
        "agreement_count": int,
        "similarity": float,
        "contradiction": dict | None,   # set if numeric_contradiction fires
        "superseded_by": dict | None,   # set if recency_supersession fires
    }

    TODO: implement entailment scoring with sentence-transformers
    (e.g. all-MiniLM-L6-v2, reused from Calibr's matching engine).
    """
    raise NotImplementedError


def extract_metric_claims(text: str) -> list[dict]:
    """
    Pull (metric_name, dataset, score) triples out of a paper abstract/chunk,
    e.g. {"metric": "accuracy", "dataset": "GLUE", "score": 91.0}.

    TODO: start with regex/rule-based extraction (numbers near known dataset
    names and metric keywords); consider a lightweight NER model if regex
    proves too brittle.
    """
    raise NotImplementedError


def check_numeric_contradiction(claim_a: dict, claim_b: dict) -> bool:
    """
    Given two extracted metric claims for the same (metric, dataset) pair,
    determine if they report meaningfully different scores.

    TODO: define a tolerance threshold (small variance is normal across
    experimental runs, not a contradiction).
    """
    raise NotImplementedError
