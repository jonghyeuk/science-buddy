from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from utils.code_validator import validate_code
from utils.openai_utils import get_chat_response, generate_experiment_design
from utils.data import get_all_categories, get_category_by_id, search_topics

app = FastAPI(title="사이언스버디 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 Streamlit 앱 URL로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 모델
class AccessCodeCheck(BaseModel):
    code: str

class ChatRequest(BaseModel):
    code: str
    messages: List[dict]

class TopicRequest(BaseModel):
    code: str
    category_id: Optional[str] = None
    search_term: Optional[str] = None

class ExperimentRequest(BaseModel):
    code: str
    topic: str

# 접근 코드 검증 의존성
def verify_code(request: AccessCodeCheck):
    if not validate_code(request.code):
        raise HTTPException(status_code=403, detail="유효하지 않은 접근 코드입니다.")
    return request.code

# API 엔드포인트
@app.post("/api/validate-code")
async def validate_access_code(request: AccessCodeCheck):
    """접근 코드 유효성 검사"""
    if validate_code(request.code):
        return {"valid": True}
    return {"valid": False}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """AI와 채팅"""
    if not validate_code(request.code):
        raise HTTPException(status_code=403, detail="유효하지 않은 접근 코드입니다.")
    
    response = get_chat_response(request.messages)
    return {"response": response}

@app.post("/api/categories")
async def get_categories(request: AccessCodeCheck):
    """카테고리 목록 조회"""
    if not validate_code(request.code):
        raise HTTPException(status_code=403, detail="유효하지 않은 접근 코드입니다.")
    
    categories = get_all_categories()
    return {"categories": categories}

@app.post("/api/topics")
async def get_topics(request: TopicRequest):
    """주제 조회 또는 검색"""
    if not validate_code(request.code):
        raise HTTPException(status_code=403, detail="유효하지 않은 접근 코드입니다.")
    
    if request.search_term:
        results = search_topics(request.search_term)
        return {"results": results}
    
    if request.category_id:
        category = get_category_by_id(request.category_id)
        if category:
            return {"category": category}
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")
    
    # 카테고리 ID와 검색어가 모두 없으면 모든 카테고리 반환
    return {"categories": get_all_categories()}

@app.post("/api/experiment")
async def design_experiment(request: ExperimentRequest):
    """실험 설계 생성"""
    if not validate_code(request.code):
        raise HTTPException(status_code=403, detail="유효하지 않은 접근 코드입니다.")
    
    experiment_design = generate_experiment_design(request.topic)
    return {"experiment_design": experiment_design}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
