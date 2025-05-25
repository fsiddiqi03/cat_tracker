import requests
import time
import json
from config import api_url



class API:
    def __init__(self, api_key):
        self.api_url = api_url
    



    def send_request(self, frame, file_name):
        response = requests.post(
                api_url,
                files={'image': (filename, frame, 'image/jpeg')},
                timeout=10  # Increased timeout
            )
        return response