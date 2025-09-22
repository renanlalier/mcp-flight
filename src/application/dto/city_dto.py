from dataclasses import dataclass


@dataclass
class CitySearchRequestDTO:
    """DTO for city search request"""
    keyword: str
    country_code: str | None = None
    max_results: int | None = None
    include_airports: bool = False


@dataclass
class CityDTO:
    """DTO for city"""
    name: str
    iata_code: str
    country_code: str
    country_name: str
    state_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    airports: list[dict] | None = None
