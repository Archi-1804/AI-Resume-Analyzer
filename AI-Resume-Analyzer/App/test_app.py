import unittest
import os
import sys
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from Courses import ds_course, web_course, android_course, ios_course, uiux_course
from api import app

client = TestClient(app)

class TestAIResumeAnalyzer(unittest.TestCase):

    def test_courses_data(self):
        """Test that course catalogs are populated and contain valid tuples."""
        self.assertGreater(len(ds_course), 0)
        self.assertGreater(len(web_course), 0)
        self.assertGreater(len(android_course), 0)
        self.assertGreater(len(ios_course), 0)
        self.assertGreater(len(uiux_course), 0)
        for item in ds_course:
            self.assertEqual(len(item), 2)
            self.assertTrue(item[1].startswith('http'))

    def test_pdf_reader_nonexistent_file(self):
        """Test pdf_reader raises FileNotFoundError for missing file."""
        from App import pdf_reader
        with self.assertRaises(FileNotFoundError):
            pdf_reader("nonexistent_resume.pdf")

    def test_api_root(self):
        """Test FastAPI root info endpoint returns 200 and docs links."""
        response = client.get("/api/v1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("swagger_docs", data)
        self.assertEqual(data["swagger_docs"], "/docs")


    def test_api_swagger_docs(self):
        """Test Swagger UI endpoint returns 200 HTML."""
        response = client.get("/docs")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

    def test_api_health(self):
        """Test health endpoint."""
        response = client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")

    def test_api_courses(self):
        """Test courses API endpoint."""
        response = client.get("/api/v1/courses?category=ds")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["category"], "Data Science")
        self.assertGreater(len(data["courses"]), 0)

    def test_api_feedback(self):
        """Test feedback API endpoint."""
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "score": 5,
            "comments": "Automated test feedback"
        }
        response = client.post("/api/v1/feedback", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

if __name__ == '__main__':
    unittest.main()
