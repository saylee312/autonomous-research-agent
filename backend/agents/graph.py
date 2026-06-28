from langgraph.graph import (
    StateGraph,
    END
)

from backend.agents.state import (
    ResearchState
)

from backend.agents.nodes.planner import (
    planner_node
)

from backend.agents.nodes.researcher import (
    researcher_node
)

from backend.agents.nodes.synthesizer import (
    synthesizer_node
)

from backend.agents.nodes.report_writer import (
    report_writer_node
)


def build_research_graph():

    graph = StateGraph(
        ResearchState
    )

    graph.add_node(
        "planner",
        planner_node
    )

    graph.add_node(
        "researcher",
        researcher_node
    )

    graph.add_node(
        "synthesizer",
        synthesizer_node
    )

    graph.add_node(
        "report_writer",
        report_writer_node
    )

    graph.set_entry_point(
        "planner"
    )

    graph.add_edge(
        "planner",
        "researcher"
    )

    graph.add_edge(
        "researcher",
        "synthesizer"
    )

    graph.add_edge(
        "synthesizer",
        "report_writer"
    )

    graph.add_edge(
        "report_writer",
        END
    )

    return graph.compile()