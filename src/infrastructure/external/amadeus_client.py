import httpx
import logging
from typing import Dict, Any
from src.infrastructure.external.amadeus_auth import AmadeusAuthService
from src.infrastructure.config.settings import config
from src.domain.exceptions.flight_exceptions import (
    FlightApiException, 
    FlightServiceUnavailableException,
    InvalidSearchParametersException
)

logger = logging.getLogger(__name__)


class AmadeusClient:
    """Client for Amadeus API"""
    
    def __init__(self):
        self._auth_service = AmadeusAuthService()
    
    async def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Makes GET request to Amadeus API"""
        url = f"{config.amadeus.api_base}{endpoint}"
        access_token = await self._auth_service.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, headers=headers, params=params or {})
                
                if response.status_code == 401:
                    # Token expired, try to renew
                    self._auth_service.invalidate_token()
                    access_token = await self._auth_service.get_access_token()
                    headers = {"Authorization": f"Bearer {access_token}"}
                    response = await client.get(url, headers=headers, params=params or {})
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error("HTTP error in Amadeus API: %s - %s", e.response.status_code, str(e))
                
                if e.response.status_code == 400:
                    raise InvalidSearchParametersException(f"Invalid parameters: {e.response.text}") from e
                elif e.response.status_code >= 500:
                    raise FlightServiceUnavailableException("Service temporarily unavailable") from e
                else:
                    raise FlightApiException(f"API error (HTTP {e.response.status_code})", e.response.status_code) from e
                    
            except (httpx.RequestError, ConnectionError) as e:
                logger.error("Connectivity error: %s", str(e))
                raise FlightServiceUnavailableException("Connectivity error. Please try again.") from e
