import requests
import time
from typing import Dict, Optional, Any
from pathlib import Path

class TMDBClient:

    base_url = "https://api.themoviedb.org/3"

    def __init__(self, api_key: str, delay = 0.05):
        self.api_key = api_key
        self.session = requests.Session()
        self.delay = delay
    
    def _get(self, endpoint: Path | str, params: Optional[Dict] = None) -> Dict[str, Any]:
        if params is None:
            params = {}

        params['api_key'] = self.api_key

        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url=url, params=params)
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}")
        
        time.sleep(self.delay)
        return response.json()

