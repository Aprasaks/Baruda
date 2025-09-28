# Python 기반 이미지 사용 (가볍고 안정적인 slim 버전을 추천)
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치 (캐싱 효율을 높임)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 코드 복사
COPY . .

# FastAPI 서버가 사용할 포트 노출 (Docker 컨테이너 내부 포트)
EXPOSE 8000

# 서버 실행 명령어 (개발 환경용)
# Uvicorn을 사용하여 main.py 파일의 app 객체를 띄움
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]