# LocalHub

> 공공데이터 기반 구미·경북 지역 정보 탐색 및 익명 커뮤니티 서비스

LocalHub는 구미·경북권의 공공 관광 데이터를 기반으로 장소를 탐색하고, 지역 주민과 방문자가 익명으로 경험을 공유할 수 있는 웹 서비스입니다. 장소 데이터는 SQLite에 적재하여 FastAPI REST API로 제공하고, 프론트엔드는 Vue 3 SPA로 구성했습니다. 사용자는 장소 목록·상세·지도 탐색, 익명 게시판 CRUD, 지역 정보 챗봇을 통해 분산된 지역 정보를 한곳에서 확인할 수 있습니다.

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 서비스명 | LocalHub |
| 선정 권역 | 구미·경북 |
| 핵심 문제 | 분산된 지역 정보를 쉽게 탐색하고, 지역 경험을 익명으로 공유할 통합 플랫폼 필요 |
| 주요 사용자 | 구미·경북 방문 관광객, 지역 주민, 회원가입 없이 이용하고 싶은 익명 사용자 |
| 개발 기간 | 2026.07.14 ~ 2026.07.16 |
| 프론트엔드 | Vue 3, Vite, JavaScript, Vue Router, Tailwind CSS v4, Leaflet |
| 백엔드 | FastAPI, SQLAlchemy, SQLite |
| AI | OpenAI API 기반 지역 정보 챗봇 |
| 배포 | Netlify(Frontend), Render(Backend) |

---

## 2. 핵심 기능

### 2.1 장소 탐색

- 제공 JSON 데이터를 SQLite에 적재
- 구미·경북 장소 1,667건 활용
- 카테고리별 장소 탐색
- 장소명·주소 기반 검색
- 페이지네이션
- 장소 상세 조회
- 장소 조회수 증가
- 장소 좋아요 기능
- 이미지 누락 및 로딩 실패 fallback 처리

### 2.2 지도 기반 탐색

- Leaflet + OpenStreetMap 지도 시각화
- 장소 위도·경도 기반 마커 표시
- 지도 마커와 장소 목록 선택 상태 연동
- 장소 상세 위치 지도 제공
- 주변 장소 추천
- Haversine 거리 계산 기반 가까운 장소 정렬

### 2.3 익명 커뮤니티

- 회원가입 없는 익명 게시판
- 게시글 목록 조회
- 게시글 상세 조회
- 게시글 작성
- 게시글 수정
- 게시글 삭제
- 비밀번호 기반 수정·삭제 검증
- 게시글 검색
- 게시글 카테고리 필터
- 조회수 증가
- 비밀번호 필드 응답 제외

### 2.4 지역 정보 챗봇

- 우측 하단 플로팅 챗봇 UI
- 대화 히스토리 유지
- 추천 질문 제공
- 모바일 대응
- `/api/chat` 엔드포인트 연동
- DB 장소 데이터 기반 후보 검색
- OpenAI API 기반 자연어 응답
- 답변 관련 장소 reference 링크 제공
- API Key 미설정 시 안전한 fallback 응답

---

## 3. 구현 포인트

### 실제 데이터 기반 서비스

단순 Mock 화면이 아니라 구미·경북 관광 JSON 데이터를 SQLite에 적재하고, 실제 장소 1,667건을 검색·필터·상세·지도에 연결했습니다.

### 화면과 API 사이의 Mapper 계층

백엔드의 snake_case 응답과 프론트 화면 모델을 분리하기 위해 `placeMapper`, `postMapper`를 두었습니다. API 응답 필드가 달라져도 화면 컴포넌트 수정 범위를 줄일 수 있습니다.

### 지도 선택 기능의 실질적 활용

선택 기능으로 Leaflet 지도를 단순 표시하는 데 그치지 않고, 장소 목록과 마커의 선택 상태를 연결하고, 상세 화면에서는 가까운 장소를 거리순으로 추천합니다.

### 익명 커뮤니티의 MVP 요구사항 충족

로그인 없이 게시글을 작성하고, 비밀번호로 수정·삭제 권한을 확인합니다. 교육 목적 요구사항에 맞게 평문 비밀번호 비교 구조를 유지하되 응답에는 비밀번호를 포함하지 않습니다.

### DB 기반 챗봇

챗봇은 질문을 그대로 OpenAI에 보내는 방식이 아니라, SQLite 장소 데이터에서 관련 후보를 먼저 찾고, 검색된 데이터만 기반으로 답하도록 제한했습니다. 이를 통해 없는 장소나 운영 정보를 지어내는 위험을 줄였습니다.

### 예외 상태 대응

로딩, 빈 결과, API 오류, 이미지 없음, 좌표 없음, 잘못된 ID, 비밀번호 불일치 등 실제 데이터 연결 후 발생할 수 있는 상태를 UI에서 처리합니다.

---

## 4. 데이터 현황

| 구분 | 건수 |
|---|---:|
| 전체 장소 | 1,667 |
| 관광지 | 499 |
| 쇼핑 | 411 |
| 음식점 | 394 |
| 문화시설 | 112 |
| 레포츠 | 110 |
| 숙박 | 80 |
| 여행코스 | 31 |
| 축제공연행사 | 30 |

> 데이터는 제공 JSON을 기반으로 하며, 추가 데이터 사용 시 라이선스 및 공공누리 유형 확인이 필요합니다.

---

## 5. 주요 화면

| 화면 | 설명 |
|---|---|
| 홈 | 서비스 소개, 카테고리 탐색, 추천 장소, 지도 탐색, 커뮤니티 미리보기 |
| 장소 둘러보기 | 장소 검색, 카테고리 필터, 페이지네이션, 카드형 목록 |
| 장소 상세 | 장소 이미지, 기본 정보, 설명, 위치 지도, 주변 장소 추천 |
| 커뮤니티 목록 | 게시글 검색, 카테고리 필터, 페이지네이션, 글쓰기 이동 |
| 게시글 상세 | 제목, 본문, 위치, 조회수, 수정·삭제 메뉴, 비밀번호 모달 |
| 게시글 작성·수정 | 제목, 내용, 카테고리, 관련 장소, 비밀번호 입력 |
| 챗봇 | 지역 정보 질문, 추천 질문, 관련 장소 링크 |

---

## 6. 프로젝트 구조

```text
LocalHub/
├─ fe/                         # Vue 3 프론트엔드
│  ├─ src/
│  │  ├─ api/                  # Axios API 계층
│  │  ├─ components/           # 공통, 홈, 장소, 게시판, 챗봇 컴포넌트
│  │  ├─ data/                 # 개발용 Mock 데이터
│  │  ├─ router/               # Vue Router
│  │  ├─ views/                # 페이지 단위 View
│  │  └─ assets/               # 전역 CSS
│  └─ package.json
│
└─ be/                         # FastAPI 백엔드
   ├─ app/
   │  ├─ api/routers/          # locations, posts, chat 등 API 라우터
   │  ├─ ai/                   # 챗봇 검색 및 OpenAI 호출 로직
   │  ├─ core/                 # 환경변수 및 설정
   │  ├─ db/                   # SQLAlchemy 세션/베이스
   │  ├─ models/               # Place, Post 모델
   │  ├─ prompts/              # 챗봇 시스템 프롬프트
   │  └─ main.py
   ├─ data/                    # 제공 JSON 데이터
   ├─ database/localhub.db     # SQLite DB
   └─ tests/                   # API 테스트
```

---

## 7. 실행 방법

### 7.1 Backend

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

백엔드 실행 후 Swagger 확인:

```text
http://127.0.0.1:8000/docs
```

### 7.2 Frontend

```bash
cd fe
npm install
npm run dev
```

프론트 실행:

```text
http://localhost:5173
```

---

## 8. 환경변수

### 8.1 Frontend `.env`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### 8.2 Backend `.env`

```env
DATABASE_URL=sqlite:///./database/localhub.db
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5-mini
TOUR_API_SERVICE_KEY=your_tour_api_key
```

> `.env`는 Git에 포함하지 않습니다. `.env.example`만 공유하는 것을 권장합니다.

---

## 9. API 요약

### 장소 API

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/api/locations` | 장소 목록 조회, 검색, 카테고리 필터, 페이지네이션 |
| GET | `/api/locations/{id}` | 장소 상세 조회 및 조회수 증가 |
| GET | `/api/locations/{id}/nearby` | 주변 장소 조회 |
| POST | `/api/locations/{id}/like` | 장소 좋아요 |
| DELETE | `/api/locations/{id}/like` | 장소 좋아요 취소 |
| GET | `/api/locations/ranking` | 조회수·좋아요·게시글 기반 인기 장소 |

### 게시글 API

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/api/posts` | 게시글 목록 조회, 검색, 카테고리 필터 |
| GET | `/api/posts/{id}` | 게시글 상세 조회 및 조회수 증가 |
| POST | `/api/posts` | 게시글 작성 |
| PUT | `/api/posts/{id}` | 게시글 수정 |
| DELETE | `/api/posts/{id}` | 게시글 삭제 |
| POST | `/api/posts/{id}/verify-password` | 비밀번호 검증 |

### 챗봇 API

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/chat` | 장소 데이터 기반 챗봇 응답 생성 |

---

## 10. 테스트

백엔드 테스트 파일은 `be/tests`에 위치합니다.

```bash
cd be
python -m unittest discover tests
```

주요 검증 항목:

- 장소 목록·상세·주변 장소 API
- 장소 랭킹 API
- 게시글 CRUD 및 비밀번호 검증
- 게시글 응답에서 password 제외
- 챗봇 응답 및 OpenAI Key 미설정 fallback
- CORS 및 오류 처리
- 관광공사 상세 API 프록시

---

## 11. 향후 개선 방향

- Render 배포 환경에서 SQLite 초기 데이터 유지 전략 보완
- 챗봇 검색 후보에 게시글 데이터까지 포함
- 장소 랭킹 UI 고도화
- 좋아요 중복 방지 방식 개선
- OpenAI 연결 실패 시 fallback 답변 품질 개선
- 데이터 출처·라이선스 문서화 강화

--- 

## 12. 발표 자료
https://gamma.app/docs/-rpr0kepf3rnw66j