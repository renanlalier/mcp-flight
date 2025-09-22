from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.city import City
from src.domain.vo.search_params import CitySearchParams


class CityGateway(ABC):
    """City gateway interface for external API"""
    
    @abstractmethod
    async def search_cities(self, params: CitySearchParams) -> dict:
        """Search cities via external API"""
        pass
