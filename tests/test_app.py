import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
	def setUp(self):
		self.client = app.test_client()
	def test_home(self):
		response = self.client.get('/')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert "<title>Home</title>" in html
		assert '<h2>About Me</h2>' in html

	def test_timeline(self):
		response = self.client.get('/api/timeline_post')
		assert response.status_code == 200
		assert response.is_json
		json = response.get_json()
		assert "timeline_posts" in json
		assert len(json["timeline_posts"]) == 0

		response = self.client.post('/api/timeline_post', data={'name': 'John', 'email':'john@example.com', 'content':'Hello world, I am John!'})
		assert response.status_code == 200
		response = self.client.get('/api/timeline_post')
		assert response.status_code == 200
		assert response.is_json
		json = response.get_json()
		assert len(json['timeline_posts']) == 1

		response = self.client.get('/timeline')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert '<title>Timeline</title>' in html

	def test_malformed_timeline_post(self):
		#post w/ no name
		response = self.client.post('/api/timeline_post', data={'email':'john@example.com', 'content':'Hello world, I am John!'})
		assert response.status_code == 400
		html = response.get_data(as_text=True)
		assert "Invalid name" in html

		#post with empty content
		response = self.client.post('/api/timeline_post', data={'name': 'John Doe', 'email': 'john@example.com', 'content': ''})
		assert response.status_code == 400
		html = response.get_data(as_text=True)
		assert "Invalid content" in html

		#post request with malformed email
		response = self.client.post('api/timeline_post', data={'name': 'John Doe', 'email': 'not-an-email', 'content': 'Hello world I\'m John!'})
		assert response.status_code == 400
		html = response.get_data(as_text=True)
		assert 'Invalid email' in html
