from fastapi import APIRouter, HTTPException
from models import AnalyzeRequest,AnalyzeResponse
from insights.llm import analyze

router = APIRouter()

@router.post("/analyze",response_model=AnalyzeResponse)
async def analyze_route(req: AnalyzeRequest):
    try:
        insights = await analyze(req.url)
    except Exception as e:
        print(f"EXCEPTION TYPE: {type(e).__name__}, MESSAGE: {e!r}")
        raise HTTPException(status_code=422, detail=f"{type(e).__name__}: {e}")
    return AnalyzeResponse(url=req.url,**insights.model_dump())
