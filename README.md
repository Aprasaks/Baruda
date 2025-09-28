# 🐳 Baruda: 개발자 지식 기반 LLM 멘토 (RAG System)

Baruda는 Docker 컨테이너 환경에서 Next.js (FE)와 FastAPI (BE)를 분리하여 운영하며, 오픈소스 LLM (Ollama)과 RAG (검색 증강 생성) 기술을 결합한 지식 기반 멘토 시스템입니다.

## 1. 9월 28일 (토) 개발 환경 구축 상세 기록

프로젝트의 가장 중요한 기반 환경 설정 및 Git 연동 작업을 완료했습니다. 이 과정에서 **Docker 환경에 대한 이해**를 높이고, 현업 수준의 **재현 가능한 개발 환경**을 구축하는 데 성공했습니다.

| **09:00 ~ 13:00** | **프로젝트 구조 및 파일 생성** | `Baruda` 최상위 폴더 생성. `frontend/`, `backend/`, `docs/` 폴더 분리. `npm create next-app` 및 `backend` 필수 파일 (`main.py`, `requirements.txt`) 생성. |
| **13:00 ~ 15:00** | **Docker 환경 파일 작성** | `frontend/Dockerfile`, `backend/Dockerfile` 작성 완료. FE/BE/Ollama를 통합 관리할 핵심 `docker-compose.yml` 파일 작성 완료. |
| **15:00 ~ 17:00** | **최소 통합 환경 구현** | FE/BE에 **최소 동작 코드(FastAPI Mock API 포함)** 주입. `requirements.txt`에 `fastapi`, `uvicorn` 추가. |
| **17:00 ~ 20:00** | **Docker 환경 실행 및 디버깅** | `docker-compose up` 실행 과정에서 명령어 인식 오류 및 `network_mode` 충돌 오류 발생. `docker-compose.yml` 수정 및 명령어(`docker-compose`로 변경)를 통해 오류 해결. **FE, BE, Ollama 3-Tier 서비스 동시 실행 성공.** |
| **20:00 ~ 21:00** | **Git 연동 및 최종 푸시** | GitHub에 원격 레포지토리 생성 후, 로컬 저장소와 연결(`git remote add origin...`). 최초 **커밋 기록 누락** 오류 해결 후, 전체 환경 설정 내용을 GitHub에 성공적으로 푸시하여 개발 시작점 확정. |

---

## 2. 개발 계획 (로드맵)

| **Phase 1** | **FE 디자인 및 Mock 연동 완성** | 사용자 친화적인 UI/UX 디자인 완성. 질문/답변/출처 시각화 컴포넌트 개발. FE가 BE의 Mock API를 호출하여 디자인이 깨지지 않는지 확인. |
| **Phase 2** | **BE RAG Core 구현** | `docs/` 지식 문서를 `langchain`으로 청크(Chunk) 처리 및 임베딩. `ChromaDB`에 벡터 저장소 구축. `/ask` 엔드포인트에 **Ollama 추론**을 결합한 RAG 파이프라인 구현. |
| **Phase 3** | **통합 및 테스트** | FE와 BE의 최종 통합 테스트. RAG 성능 평가 및 지식 기반의 답변 정확도 검증. 에러 처리 로직 및 사용자 경험 개선. |
| **Phase 4** | **배포 (Deployment)** | Docker 이미지를 활용하여 클라우드 서비스(예: AWS ECS, GCP Cloud Run)에 배포하여 프로젝트 완성도를 높임. |

---

## 3. FE / BE / Docker 개발 구조 및 역할

Baruda 프로젝트는 현대적인 웹 서비스 개발 구조를 따르며, 각 역할은 아래 기술.

### Frontend (FE) - Next.js (Port 3000)

- **기술 스택:** Next.js (React), TypeScript, Tailwind CSS
- **역할:** 사용자 인터페이스(UI) 및 사용자 경험(UX) 전담. 사용자 질문을 받아 **FastAPI (BE)**로 전달하고, BE가 반환한 답변(`answer`) 및 **출처 목록(`sources`)**을 시각적으로 구현합니다. 국비 과정에서 습득한 디자인 및 반응형 웹 기술을 집중적으로 적용합니다.

### Backend (BE) - FastAPI (Port 8000)

- **기술 스택:** Python, FastAPI, LangChain, ChromaDB
- **역할:** RAG(검색 증강 생성) 로직의 핵심 두뇌.
  1.  **API 서버:** FE의 요청을 받고 응답하는 RESTful API 제공.
  2.  **RAG 엔진:** 질문을 벡터 검색 후, Ollama를 통해 최종 답변을 생성하고 사용된 **출처 목록(Source List)**을 함께 FE로 전송합니다.

### Docker Environment

- **역할:** **FE와 BE의 개발 환경을 독립적으로 격리**하고 통합합니다.
  - `docker-compose.yml`이 세 개의 서비스(FE, BE, Ollama)를 하나의 명령어로 동시 실행 및 관리합니다.
  - `backend` 컨테이너가 `ollama` 서비스 이름(`http://ollama:11434`)을 통해 LLM에 접근하도록 네트워크를 설정했습니다.

---

## 4. 🐳 Docker 도입 배경 및 중요성 (첫 사용)

이 프로젝트에 Docker를 도입한 것은 단순한 기술적 과시가 아닌, **필수적인 설계 결정**이었습니다. 이번 프로젝트가 Docker를 처음 사용해 보는 경험이지만, 그 중요성 때문에 도입했습니다.

### 도입 이유

1.  **환경 일치성 (Reproducible Environment):**

    - **문제:** FE(Node.js/npm)와 BE(Python/pip)는 서로 다른 운영체제 종속성과 라이브러리를 가집니다. 심지어 BE는 Ollama라는 **LLM 런타임**까지 필요합니다.
    - **해결:** Docker는 이 모든 환경을 **격리된 컨테이너**에 담아, 개발자 PC, 심사관 PC, 클라우드 서버 등 **어디서든 동일한 환경에서 동일한 결과**가 나오도록 보장합니다.

2.  **종속성 및 버전 관리의 단순화:**

    - `Dockerfile` 안에 `npm install`이나 `pip install` 과정을 명시함으로써, 개발자가 환경 설정에 시간을 낭비하지 않고 **`docker-compose up` 한 번**으로 모든 준비를 끝낼 수 있습니다.

3.  **현업 적합성 (DevOps Competency):**
    - 최근의 IT 환경에서는 **컨테이너 기반 배포**가 표준입니다. Docker를 사용하여 프로젝트를 구축함으로써, **DevOps 파이프라인과 현대적인 클라우드 배포 흐름**에 대한 기본 이해와 실습 능력을 증명할 수 있습니다.

Docker 덕분에 복잡한 RAG 시스템을 안정적으로 구축하고, 향후 클라우드 배포 단계(Phase 4)로의 전환이 용이해졌습니다.

## 5. 프로젝트 시작 이유

이전에도 유사한 블로그 기반 AI 질의응답 시스템을 구축하려 시도했으나, OpenAI 등 상용 LLM API를 사용했을 때 다음과 같은 문제에 직면했습니다.

환각 (Hallucination) 현상 심화: AI가 블로그 내용이 아닌, 방대한 일반 인터넷 지식을 섞어 답변하는 정보의 간섭 문제 발생.

지식 통제 실패: AI가 "딱 내 블로그 글만" 가지고 답변하도록 강제하는 데 실패.

이러한 문제들을 겪으며, 단순한 API 호출로는 도메인 특화된 AI를 구현할 수 없다는 결론에 도달했습니다.

이번 Baruda 프로젝트는 이러한 실패 경험을 바탕으로, 정보의 출처를 완벽히 통제하고 정확한 근거를 제시하는 RAG 아키텍처만이 해답임을 깨닫고 시작된 프로젝트입니다.

단순히 코드를 짜는 것을 넘어, 문제가 왜 발생했고, 그 문제를 해결하기 위해 어떤 아키텍처가 필요한지를 탐구하는 새로운 도전이자 동력이 될 것입니다.
