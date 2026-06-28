from typing import TypedDict
from typing import List


class ResearchState(TypedDict):

    query: str

    plan: List[str]

    research_results: List[str]

    synthesized_content: str

    report: str