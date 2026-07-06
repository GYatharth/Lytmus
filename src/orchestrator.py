"""
Agent orchestrator: routes sub-questions to the right retrieval tool(s)
(web search, local corpus, or both) and merges results before synthesis.
"""


def run_pipeline(query: str) -> dict:
    """
    Full pipeline entrypoint: plan -> retrieve -> synthesize -> score.

    TODO: implement as a LangChain tool-calling agent (ChatGroq + bind_tools),
    or a LangGraph state machine if branching logic gets complex.
    """
    raise NotImplementedError
