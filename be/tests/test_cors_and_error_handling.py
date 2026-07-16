import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.services.openai_service import OpenAIServiceError


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


class CorsAndErrorHandlingTest(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)

    def test_cors_preflight_allows_deployed_frontend(self):
        frontend_origin = "https://localhub3team.netlify.app/"

        response = self.client.options(
            "/api/posts",
            headers={
                "Origin": frontend_origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["access-control-allow-origin"],
            frontend_origin,
        )
        self.assertIn(
            "POST",
            response.headers["access-control-allow-methods"],
        )

    def test_cors_preflight_allows_local_frontend(self):
        frontend_origin = "http://localhost:5173"

        response = self.client.options(
            "/api/posts",
            headers={
                "Origin": frontend_origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["access-control-allow-origin"],
            frontend_origin,
        )

    def test_create_post_rejects_blank_required_fields_with_400(self):
        response = self.client.post(
            "/api/posts",
            json={
                "title": "   ",
                "content": "   ",
                "category": "   ",
                "location_name": "",
                "password": "   ",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "title, content, category, and password are required",
        )

    def test_update_post_missing_password_returns_400(self):
        create_response = self.client.post(
            "/api/posts",
            json={
                "title": "원본 제목",
                "content": "원본 내용",
                "category": "여행후기",
                "location_name": "금오산",
                "password": "1234",
            },
        )
        post_id = create_response.json()["id"]

        response = self.client.put(
            f"/api/posts/{post_id}",
            json={
                "title": "수정 제목",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "password is required")

    def test_delete_post_wrong_password_returns_403(self):
        create_response = self.client.post(
            "/api/posts",
            json={
                "title": "원본 제목",
                "content": "원본 내용",
                "category": "여행후기",
                "location_name": "금오산",
                "password": "1234",
            },
        )
        post_id = create_response.json()["id"]

        response = self.client.request(
            "DELETE",
            f"/api/posts/{post_id}",
            json={"password": "wrong"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "password mismatch")

    def test_location_missing_id_returns_404(self):
        response = self.client.get("/api/locations/999999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "location not found")

    def test_chat_empty_message_returns_400(self):
        response = self.client.post("/api/chat", json={"message": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "message is required")

    def test_chat_service_error_returns_safe_guidance(self):
        with patch(
            "app.api.routers.chat.OpenAIService.generate_answer",
            side_effect=OpenAIServiceError("SECRET_API_KEY"),
        ):
            response = self.client.post("/api/chat", json={"message": "hello"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["answer"],
            "현재 제공된 데이터에서는 확인되지 않습니다.",
        )
        self.assertNotIn("SECRET_API_KEY", response.text)


if __name__ == "__main__":
    unittest.main()