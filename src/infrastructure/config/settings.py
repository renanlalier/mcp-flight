import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AmadeusConfig:
    """Amadeus API configuration"""
    api_base: str
    api_key: str
    api_secret: str
    
    @classmethod
    def from_env(cls) -> 'AmadeusConfig':
        """Create configuration from environment variables"""
        api_key = os.getenv('AMADEUS_API_KEY')
        api_secret = os.getenv('AMADEUS_API_SECRET')
        api_base = os.getenv('AMADEUS_API_BASE', 'https://test.api.amadeus.com')
        
        if not api_key:
            raise ValueError("AMADEUS_API_KEY environment variable is required")
        if not api_secret:
            raise ValueError("AMADEUS_API_SECRET environment variable is required")
            
        return cls(
            api_base=api_base,
            api_key=api_key,
            api_secret=api_secret
        )


@dataclass
class AppConfig:
    """Application configuration"""
    templates_dir: Path = Path(__file__).parent.parent.parent / "presentation" / "templates"
    amadeus: AmadeusConfig | None = None
    
    def __post_init__(self):
        if self.amadeus is None:
            self.amadeus = AmadeusConfig.from_env()


# Global configuration instance
config = AppConfig()
