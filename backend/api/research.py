from fastapi import APIRouter

from backend.agents.graph import build_research_graph

from backend.services.report_service import ReportService


router = APIRouter()

graph = build_research_graph()
report_service = ReportService()


@router.post("/generate-report")
async def generate_report(payload: dict):

    query = payload["query"]

    result = graph.invoke({"query": query})

    report = report_service.save_report(
        title=query,
        content=result["report"],
        report_type="pdf"
    )

    return {
        "report_id": report["_id"],
        "report": result["report"]
    }