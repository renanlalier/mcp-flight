from typing import List
from src.domain.gateways.city_gateway import CityGateway
from src.domain.vo.search_params import CitySearchParams
from src.application.dto.city_dto import CitySearchRequestDTO, CityDTO


class CityApplicationService:
    """Application service for cities"""
    
    def __init__(self, city_gateway: CityGateway):
        self._city_gateway = city_gateway
    
    async def search_cities(self, request: CitySearchRequestDTO) -> List[CityDTO]:
        """Searches cities and returns DTOs"""
        params = CitySearchParams(
            keyword=request.keyword,
            country_code=request.country_code,
            max_results=request.max_results,
            include="AIRPORTS" if request.include_airports else None
        )
        
        cities = await self._city_gateway.search_cities(params)
        
        return [self._map_city_to_dto(city) for city in cities]
    
    def _map_city_to_dto(self, city) -> CityDTO:
        """Maps entity to DTO"""
        airports = []
        for airport in city.airports:
            airport_dict = {
                "iata_code": airport.iata_code,
                "name": airport.name,
                "coordinates": {
                    "latitude": airport.coordinates.latitude,
                    "longitude": airport.coordinates.longitude
                } if airport.coordinates else None
            }
            airports.append(airport_dict)
        
        return CityDTO(
            name=city.name,
            iata_code=city.iata_code,
            country_code=city.country_code,
            country_name=city.country_name,
            state_code=city.state_code,
            latitude=city.coordinates.latitude if city.coordinates else None,
            longitude=city.coordinates.longitude if city.coordinates else None,
            airports=airports
        )
