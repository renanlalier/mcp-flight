import httpx
import logging
from src.infrastructure.config.settings import config
from src.domain.exceptions.flight_exceptions import (
    FlightApiException,
    FlightServiceUnavailableException,
    InvalidSearchParametersException
)

logger = logging.getLogger(__name__)


class AmadeusAuthService:
    """Amadeus authentication service"""

    def __init__(self):
        self._access_token: str | None = None
    
    async def get_access_token(self) -> str:
        """Gets valid access token"""
        if self._access_token is None:
            self._access_token = await self._fetch_new_token()
        return self._access_token
    
    async def _fetch_new_token(self) -> str:
        """Fetches new token from API"""
        url = f"{config.amadeus.api_base}/v1/security/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": config.amadeus.api_key,
            "client_secret": config.amadeus.api_secret,
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(url, headers=headers, data=data)
                response.raise_for_status()
                token_data = response.json()
                return token_data["access_token"]
                
            except httpx.HTTPStatusError as e:
                logger.error("HTTP error in Amadeus authentication: %s - %s", e.response.status_code, str(e))
                
                if e.response.status_code == 400:
                    raise InvalidSearchParametersException("Invalid API credentials") from e
                elif e.response.status_code >= 500:
                    raise FlightServiceUnavailableException("Authentication service temporarily unavailable") from e
                else:
                    raise FlightApiException(f"Authentication error (HTTP {e.response.status_code})", e.response.status_code) from e
                    
            except (httpx.RequestError, ConnectionError) as e:
                logger.error("Connectivity error in authentication: %s", str(e))
                raise FlightServiceUnavailableException("Connectivity error in authentication. Please try again.") from e
    
    def invalidate_token(self):
        """Invalidates current token"""
        self._access_token = None
