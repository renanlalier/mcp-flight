from dataclasses import dataclass
import re


@dataclass(frozen=True)
class LocationCode:
    """IATA location code"""
    code: str
    
    def __post_init__(self):
        if not self._is_valid_iata_code(self.code):
            raise ValueError(f"Invalid IATA code: {self.code}")
    
    @staticmethod
    def _is_valid_iata_code(code: str) -> bool:
        """Validates IATA code (3 uppercase letters)"""
        return bool(re.match(r'^[A-Z]{3}$', code))
    
    def __str__(self) -> str:
        return self.code
