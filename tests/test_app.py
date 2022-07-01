import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Home</title>" in html

        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h2>About Me</h2>" in html

        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h3>About Me</h3>" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_post" in json
        assert len(json["timeline_post"]) >= 0

        response = self.client.post("/api/timeline_post", data={"name": "Johnny Test", "email":"tester@example.com", "content": "Testing content"})
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "timeline_post" in html

        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<form id=\"form\">" in html


        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h1>Timeline</h1>" in html

    def test_malformed_timeline_post(self):
        #POST request missing name
        response = self.client.post("/api/timeline_post", data={"email":"john@example.com", "content": "Hello world, I'm John"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html        

        #POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name":"John","email":"john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        #POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name":"John","email":"johnexample.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html 