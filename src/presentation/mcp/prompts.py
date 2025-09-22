import logging
from mcp.server.fastmcp import FastMCP
from jinja2 import Environment, FileSystemLoader

from src.infrastructure.config.settings import config

logger = logging.getLogger(__name__)


def register_prompts(mcp: FastMCP):
    """Registers MCP prompts"""
    
    # Jinja2 configuration
    jinja_env = Environment(loader=FileSystemLoader(config.templates_dir))
    
    @mcp.prompt()
    async def vacation_prompt(
        destination: str,
        origin: str | None = None,
        duration: int | None = None,
        vacation_month: str | None = None,
        budget: int | None = None,
        interests: list[str] | None = None
    ) -> str:
        """Guides the vacation flight search process using Jinja2 template"""
        try:
            template = jinja_env.get_template('vacation_prompt.j2')
            return template.render(
                destination=destination,
                origin=origin,
                duration=duration,
                vacation_month=vacation_month,
                budget=budget,
                interests=interests
            )
        except Exception as e:
            logger.error("Error rendering template: %s", str(e))
            # Fallback to basic prompt in case of error
            return (
                f"Help the user find the best flight options from {origin or 'their location'} to {destination} "
                f"considering duration of {duration or 'not specified'} days, "
                f"vacation month of {vacation_month or 'not specified'}, "
                f"budget of {budget or 'flexible'} and interests in "
                f"{', '.join(interests) if interests else 'general activities'}. "
                f"Provide flight suggestions, best travel times and money-saving tips."
            )
    
    @mcp.prompt()
    async def prompt_flight_search(
        origin: str,
        destination: str,
        departure_date: str,
        adults: int = 1,
        return_date: str | None = None,
        children: int | None = None,
        infants: int | None = None,
        travel_class: str | None = None,
        currency_code: str | None = None,
        max_price: int | None = None,
        non_stop: bool | None = None
    ) -> str:
        """Guides specific flight search using Jinja2 template"""
        try:
            template = jinja_env.get_template('flight_search_prompt.j2')
            return template.render(
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                adults=adults,
                children=children,
                infants=infants,
                travel_class=travel_class,
                currency_code=currency_code,
                max_price=max_price,
                non_stop=non_stop
            )
        except Exception as e:
            logger.error("Error rendering flight search template: %s", str(e))
            # Basic fallback
            return (
                f"Search flights from {origin} to {destination} "
                f"departing on {departure_date} "
                f"for {adults} adult(s). "
                f"Use search tools to find the best options."
            )
