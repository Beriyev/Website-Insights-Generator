from fastapi import APIRouter, HTTPException
from models import AnalyzeRequest,AnalyzeResponse
from insights.llm import analyze

router = APIRouter()

@router.post("/analyze",response_model=AnalyzeResponse)
async def analyze_route(req: AnalyzeRequest):
    try:
        insights = await analyze(req.url)
    except Exception as e:
        raise HTTPException(status_code=422,detail="Could not Analyze.")
    return AnalyzeResponse(url=req.url,**insights.model_dump())