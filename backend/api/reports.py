import time

from fastapi import (
    APIRouter,
    HTTPException
)

from fastapi.responses import (
    FileResponse
)

from pydantic import BaseModel

from backend.agents.graph import build_research_graph
from backend.services.report_service import (
    ReportService
)


class GenerateReportRequest(BaseModel):
    query: str


router = APIRouter()

graph = build_research_graph()
service = ReportService()


@router.get("/")
async def list_reports():

    return service.list_reports()


@router.post("/generate-report")
async def generate_report(payload: GenerateReportRequest):

    query = payload.query
    
    if not query or not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    # 1. Run LangGraph with timing
    try:
        print(f"\n[TIMING] Starting report generation for: {query}")
        start_time = time.time()
        
        result = graph.invoke({
            "query": query
        })
        
        graph_time = time.time() - start_time
        print(f"[TIMING] Graph execution completed in {graph_time:.2f}s")
        
    except Exception as exc:
        error_msg = str(exc)
        
        # Better error messages for common issues
        if "429" in error_msg or "rate" in error_msg.lower():
            raise HTTPException(
                status_code=429,
                detail="External APIs are rate limiting. Please try again in a few minutes."
            )
        
        raise HTTPException(
            status_code=502,
            detail=f"Report generation failed: {error_msg}"
        )

    # 2. Save report with timing
    try:
        save_start = time.time()
        
        report_content = result.get("report", "")
        
        report = service.save_report(
            title=query,
            content=report_content,
            report_type="pdf"
        )
        
        save_time = time.time() - save_start
        print(f"[TIMING] Report saved in {save_time:.2f}s")
        print(f"[DEBUG] Report ID: {report['_id']}")
        print(f"[DEBUG] Report Title: {report['title']}")
        print(f"[DEBUG] Content length: {len(report_content)}")
        print(f"[TIMING] Total time: {graph_time + save_time:.2f}s\n")
        
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save report: {str(exc)}"
        )

    return {
        "report_id": report["_id"],
        "report": result.get("report", ""),
        "generation_time_seconds": graph_time
    }


@router.get("/{report_id}/download")
async def download_report(
    report_id: str
):

    report = (
        service.repo.get_report(
            report_id
        )
    )

    if not report:

        raise HTTPException(
            status_code=404
        )

    return FileResponse(
        report["file_path"]
    )


@router.delete("/{report_id}")
async def delete_report(
    report_id: str
):

    success = (
        service.delete_report(
            report_id
        )
    )

    if not success:

        raise HTTPException(
            status_code=404
        )

    return {
        "message": "deleted"
    }