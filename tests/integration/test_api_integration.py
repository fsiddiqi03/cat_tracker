import pytest
import requests_mock
import requests
import sys
import os
import json

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from api import API


class TestAPIIntegration:
    """Integration tests for the API class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.api_url = "https://test-api.example.com/upload"
        self.api = API(self.api_url)
        self.test_frame = b"fake_image_data_for_integration_test"
        self.test_filename = "integration_test_cat.jpg"
    
    def test_api_integration_success(self):
        """Test successful integration with mock API endpoint."""
        with requests_mock.Mocker() as m:
            # Mock successful response
            m.post(self.api_url, 
                   status_code=200, 
                   json={"status": "success", "message": "Image uploaded successfully"})
            
            # Make the request
            response = self.api.send_request(self.test_frame, self.test_filename)
            
            # Verify response
            assert response.status_code == 200
            assert response.json()["status"] == "success"
            
            # Verify request was made correctly
            assert m.called
            request = m.last_request
            assert request.method == 'POST'
            assert request.url == self.api_url
            
            # Check headers
            assert 'multipart/form-data' in request.headers['Content-Type']
    
    def test_api_integration_server_error(self):
        """Test integration with server error response."""
        with requests_mock.Mocker() as m:
            # Mock server error
            m.post(self.api_url, 
                   status_code=500, 
                   text="Internal Server Error")
            
            # Make the request
            response = self.api.send_request(self.test_frame, self.test_filename)
            
            # Verify response
            assert response.status_code == 500
            assert response.text == "Internal Server Error"
    
    def test_api_integration_authentication_error(self):
        """Test integration with authentication error."""
        with requests_mock.Mocker() as m:
            # Mock authentication error
            m.post(self.api_url, 
                   status_code=401, 
                   json={"error": "Unauthorized", "message": "Invalid API key"})
            
            # Make the request
            response = self.api.send_request(self.test_frame, self.test_filename)
            
            # Verify response
            assert response.status_code == 401
            assert response.json()["error"] == "Unauthorized"
    
    def test_api_integration_rate_limit(self):
        """Test integration with rate limiting."""
        with requests_mock.Mocker() as m:
            # Mock rate limit response
            m.post(self.api_url, 
                   status_code=429, 
                   json={"error": "Rate Limited", "retry_after": 60})
            
            # Make the request
            response = self.api.send_request(self.test_frame, self.test_filename)
            
            # Verify response
            assert response.status_code == 429
            assert response.json()["error"] == "Rate Limited"
    
    def test_api_integration_large_file(self):
        """Test integration with large file upload."""
        # Create a larger test frame
        large_frame = b"x" * (1024 * 1024)  # 1MB
        
        with requests_mock.Mocker() as m:
            # Mock successful response for large file
            m.post(self.api_url, 
                   status_code=200, 
                   json={"status": "success", "size": len(large_frame)})
            
            # Make the request
            response = self.api.send_request(large_frame, "large_cat.jpg")
            
            # Verify response
            assert response.status_code == 200
            assert response.json()["size"] == len(large_frame)
    
    def test_api_integration_timeout_handling(self):
        """Test integration timeout handling."""
        with requests_mock.Mocker() as m:
            # Mock timeout
            m.post(self.api_url, exc=requests.exceptions.Timeout)
            
            # Make the request and expect timeout
            with pytest.raises(requests.exceptions.Timeout):
                self.api.send_request(self.test_frame, self.test_filename)
    
    def test_api_integration_network_error(self):
        """Test integration network error handling."""
        with requests_mock.Mocker() as m:
            # Mock network error
            m.post(self.api_url, exc=requests.exceptions.ConnectionError)
            
            # Make the request and expect connection error
            with pytest.raises(requests.exceptions.ConnectionError):
                self.api.send_request(self.test_frame, self.test_filename)
    
    def test_api_integration_multiple_requests(self):
        """Test multiple consecutive API requests."""
        with requests_mock.Mocker() as m:
            # Mock multiple successful responses
            m.post(self.api_url, [
                {'status_code': 200, 'json': {"status": "success", "id": "1"}},
                {'status_code': 200, 'json': {"status": "success", "id": "2"}},
                {'status_code': 200, 'json': {"status": "success", "id": "3"}}
            ])
            
            # Make multiple requests
            responses = []
            for i in range(3):
                response = self.api.send_request(self.test_frame, f"cat_{i}.jpg")
                responses.append(response)
            
            # Verify all responses
            for i, response in enumerate(responses):
                assert response.status_code == 200
                assert response.json()["id"] == str(i + 1)
            
            # Verify all requests were made
            assert len(m.request_history) == 3 