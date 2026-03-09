import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from core.config import Config

class BaseClient:
    """
    The parent class for all API interactions.
    It encapsulates the 'requests' library, handles common logic like headers,
    sessions, and implements a retry mechanism for stability.
    """

    def __init__(self):
        self.base_url = Config.BASE_URL
        self.session = requests.Session()


    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def _send_request(self, method: str, endpoint: str, payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        """
        Executes the HTTP request with configured retry logic.
        """
        url = f"{self.base_url}{endpoint}"
        
        kwargs.setdefault('timeout', Config.DEFAULT_TIMEOUT)

        response = self.session.request(
            method=method,
            url=url,
            json=payload,
            headers=headers,
            **kwargs
        )
        
        return response


    def get(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        return self._send_request(method="GET", endpoint=endpoint, headers=headers, **kwargs)

    def post(self, endpoint: str, payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        return self._send_request(method="POST", endpoint=endpoint, payload=payload, headers=headers, **kwargs)

    def put(self, endpoint: str, payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        return self._send_request(method="PUT", endpoint=endpoint, payload=payload, headers=headers, **kwargs)
        
    def patch(self, endpoint: str, payload: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        return self._send_request(method="PATCH", endpoint=endpoint, payload=payload, headers=headers, **kwargs)

    def delete(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        return self._send_request(method="DELETE", endpoint=endpoint, headers=headers, **kwargs)