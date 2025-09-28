# Baruda/backend/main.py (최소 작동 코드)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# 프론트엔드(Next.js)와의 통신을 위한 CORS 설정 (필수!)
origins = [
    "http://localhost:3000",  # Next.js 기본 포트
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [TEST] 프론트엔드가 호출할 핵심 API 엔드포인트 정의 (현재는 Mock 데이터 반환)
@app.post("/ask")
def ask_baruda(query: dict):
    print(f"Received Query: {query.get('question')}")
    
    # 이 답변을 기반으로 FE UI를 디자인하세요.
    mock_answer = f"('{query.get('question')}'에 대한) 바루다의 답변입니다. 현재는 Mockup 데이터입니다. 이 답변을 기반으로 프론트엔드를 꾸미세요!"
    mock_sources = [
        {"title": "FastAPI 공식 문서", "location": "API Reference/Routing", "score": 0.95},
        {"title": "Next.js 튜토리얼", "location": "챕터 3: 서버 컴포넌트", "score": 0.88},
    ]

    return {
        "answer": mock_answer,
        "sources": mock_sources
    }

# [TEST] 서버 상태 확인용
@app.get("/")
def read_root():
    return {"status": "Backend Server Running (FastAPI)"}