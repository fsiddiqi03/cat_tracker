import pytest
import requests
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from api import API


class TestAPI:
    """Test cases for the API class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.api_url = "https://test-api.example.com/upload"
        self.api = API(self.api_url)
    
    def test_api_initialization(self):
        """Test that API class initializes correctly."""
        assert self.api.api_url == self.api_url
    
    @patch('api.requests.post')
    def test_send_request_success(self, mock_post):
        """Test successful image upload request."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "message": "Image uploaded"}
        mock_post.return_value = mock_response
        
        # Test data
        test_frame = b"fake_image_data"
        test_filename = "test_cat.jpg"
        
        # Call the method
        response = self.api.send_request(test_frame, test_filename)
        
        # Assertions
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]['timeout'] == 10
        
        # Check that files were passed correctly
        files = call_args[1]['files']
        assert 'image' in files
        assert files['image'][0] == test_filename
        assert files['image'][1] == test_frame
        assert files['image'][2] == 'image/jpeg'
    
    @patch('api.requests.post')
    def test_send_request_failure(self, mock_post):
        """Test failed image upload request."""
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        # Test data
        test_frame = b"fake_image_data"
        test_filename = "test_cat.jpg"
        
        # Call the method
        response = self.api.send_request(test_frame, test_filename)
        
        # Assertions
        assert response.status_code == 500
        assert response.text == "Internal Server Error"
    
    @patch('api.requests.post')
    def test_send_request_timeout(self, mock_post):
        """Test request timeout handling."""
        # Mock timeout exception
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
        
        # Test data
        test_frame = b"fake_image_data"
        test_filename = "test_cat.jpg"
        
        # Call the method and expect timeout exception
        with pytest.raises(requests.exceptions.Timeout):
            self.api.send_request(test_frame, test_filename)
    
    @patch('api.requests.post')
    def test_send_request_connection_error(self, mock_post):
        """Test connection error handling."""
        # Mock connection error
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        # Test data
        test_frame = b"fake_image_data"
        test_filename = "test_cat.jpg"
        
        # Call the method and expect connection error
        with pytest.raises(requests.exceptions.ConnectionError):
            self.api.send_request(test_frame, test_filename)
    
    def test_send_request_invalid_inputs(self):
        """Test send_request with invalid inputs."""
        # Test with None frame
        with pytest.raises(TypeError):
            self.api.send_request(None, "test.jpg")
        
        # Test with None filename
        with pytest.raises(TypeError):
            self.api.send_request(b"data", None)
        
        # Test with empty frame
        with pytest.raises(ValueError):
            self.api.send_request(b"", "test.jpg")
        
        # Test with empty filename
        with pytest.raises(ValueError):
            self.api.send_request(b"data", "") 