from dataclasses import dataclass
from src.domain.vo.coordinates import Coordinates


@dataclass
class Airport:
    """Airport entity"""
    iata_code: str
    name: str
    city_name: str
    country_code: str
    coordinates: Coordinates | None = None


@dataclass
class City:
    """City entity"""
    name: str
    iata_code: str
    country_code: str
    country_name: str
    state_code: str | None = None
    coordinates: Coordinates | None = None
    airports: list[Airport] | None = None
    
    def __post_init__(self):
        if self.airports is None:
            self.airports = []
