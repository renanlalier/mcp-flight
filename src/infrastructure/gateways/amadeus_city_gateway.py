from src.domain.gateways.city_gateway import CityGateway
from src.domain.vo.search_params import CitySearchParams
from src.infrastructure.external.amadeus_client import AmadeusClient


class AmadeusCityGateway(CityGateway):
    """City gateway implementation using Amadeus API"""
    
    def __init__(self):
        self._client = AmadeusClient()
    
    async def search_cities(self, params: CitySearchParams) -> dict:
        """Searches cities in Amadeus API"""
        api_params = self._build_api_params(params)
        response = await self._client.get("/v1/reference-data/locations/cities", api_params)
        
        return response
    
    def _build_api_params(self, params: CitySearchParams) -> dict:
        """Builds parameters for API"""
        api_params = {"keyword": params.keyword}
        
        if params.country_code:
            api_params["countryCode"] = params.country_code
        if params.max_results:
            api_params["max"] = str(params.max_results)
        if params.include:
            api_params["include"] = params.include
        
        return api_params
