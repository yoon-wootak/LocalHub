# LocalHub Backend README

> FastAPI + SQLAlchemy + SQLite 기반 LocalHub 백엔드

## 1. 기술 스택

| 구분 | 기술 |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite |
| AI | OpenAI API |
| Environment | python-dotenv |
| Test | unittest + FastAPI TestClient |
| Deploy | Render 예정 |

---

## 2. 주요 기능

### 장소 데이터

- 제공 JSON 데이터 SQLite 적재
- 장소 목록 조회
- 장소 상세 조회
- 장소 검색
- 카테고리 필터
- 페이지네이션
- 조회수 증가
- 좋아요 증가/취소
- 인기 장소 랭킹
- 주변 장소 추천

### 커뮤니티

- 게시글 목록 조회
- 게시글 상세 조회
- 게시글 작성
- 게시글 수정
- 게시글 삭제
- 비밀번호 검증
- 조회수 증가
- 검색 및 카테고리 필터
- 응답에서 password 제외

### 챗봇

- `/api/chat` 엔드포인트
- 사용자 질문 토큰화
- 유의어 기반 검색어 확장
- 장소 DB 검색
- 검색 결과 기반 OpenAI 프롬프트 생성
- 관련 장소 reference 반환
- API Key 미설정 및 데이터 미검색 fallback 응답

---

## 3. 프로젝트 구조

```text
app/
├─ ai/
│  └─ chat_bot.py
├─ api/routers/
│  ├─ chat.py
│  ├─ health.py
│  ├─ import_data.py
│  ├─ locations.py
│  ├─ places.py
│  ├─ posts.py
│  └─ tourism.py
├─ core/
│  └─ config.py
├─ db/
│  ├─ base.py
│  └─ session.py
├─ models/
│  ├─ place.py
│  └─ post.py
├─ prompts/
│  └─ localhub_chat.py
└─ main.py
```

---

## 4. 실행 방법

```bash
cd be
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install fastapi uvicorn sqlalchemy python-dotenv openai requests
uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Health Check:

```text
GET /api/health
```

---

## 5. 환경변수

`.env`:

```env
DATABASE_URL=sqlite:///./database/localhub.db
OPENAI_API_KEY=[your_openai_api_key]
OPENAI_MODEL=gpt-5-mini
TOUR_API_SERVICE_KEY=[your_tour_api_key]
```

주의:

- `.env`는 Git에 포함하지 않습니다.
- Render 배포 시 환경변수로 등록합니다.

---

## 6. Database Schema

### places

| 컬럼 | 설명 |
|---|---|
| id | 내부 PK |
| content_id | 관광공사 콘텐츠 ID |
| content_type_id | 관광공사 콘텐츠 타입 ID |
| title | 장소명 |
| content_type | 카테고리 |
| addr1, addr2 | 주소 |
| tel | 전화번호 |
| latitude, longitude | 지도 좌표 |
| firstimage, firstimage2 | 이미지 URL |
| view_count | 상세 조회수 |
| like_count | 좋아요 수 |
| keywords | 챗봇 검색용 키워드 |

### posts

| 컬럼 | 설명 |
|---|---|
| id | 게시글 ID |
| title | 제목 |
| content | 내용 |
| category | 게시글 카테고리 |
| location_name | 관련 장소명 |
| place_id | 장소 FK |
| password | 수정·삭제용 비밀번호 |
| view_count | 조회수 |
| created_at | 생성일 |
| updated_at | 수정일 |

---

## 7. API 명세 요약

### Locations

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/api/locations` | 장소 목록 조회 |
| GET | `/api/locations/{location_id}` | 장소 상세 조회 |
| GET | `/api/locations/{location_id}/nearby` | 주변 장소 조회 |
| POST | `/api/locations/{location_id}/like` | 좋아요 |
| DELETE | `/api/locations/{location_id}/like` | 좋아요 취소 |
| GET | `/api/locations/ranking` | 인기 장소 랭킹 |

### Posts

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/api/posts` | 게시글 목록 조회 |
| GET | `/api/posts/{post_id}` | 게시글 상세 조회 |
| POST | `/api/posts` | 게시글 작성 |
| PUT | `/api/posts/{post_id}` | 게시글 수정 |
| DELETE | `/api/posts/{post_id}` | 게시글 삭제 |
| POST | `/api/posts/{post_id}/verify-password` | 비밀번호 확인 |

### Chat

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/chat` | 지역 정보 챗봇 응답 |

### Import / Tourism

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/import` | 제공 JSON 데이터 적재 |
| GET | `/api/tourism/common` | 관광공사 상세 공통 정보 프록시 |
| GET | `/api/tourism/intro` | 관광공사 상세 소개 정보 프록시 |

---

## 8. 백엔드 구현 포인트

- SQLite 파일 기반으로 배포 복잡도를 낮춘 구조
- 제공 JSON을 DB로 적재하여 프론트가 일관된 REST API로 사용 가능
- 장소 조회수, 좋아요, 게시글 수를 조합한 인기 장소 랭킹 제공
- Haversine 공식으로 주변 장소 거리 계산
- 게시글 응답에서 password 필드 제외
- 비밀번호 불일치 시 403으로 명확한 권한 오류 처리
- OpenAI 호출 전 DB 후보를 먼저 검색해 hallucination 위험 감소
- 테스트 코드로 주요 API 동작 검증

---

## 9. 테스트

```bash
cd be
python -m unittest discover tests
```

테스트 범위:

- 게시글 모델 컬럼 확인
- 게시글 CRUD
- 비밀번호 검증
- 장소 목록·상세·랭킹
- 챗봇 fallback 및 reference 반환
- CORS 설정
- 관광공사 API 요청 파라미터