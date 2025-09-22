import logging
import aiofiles
from pathlib import Path
from mcp.server.fastmcp import FastMCP


logger = logging.getLogger(__name__)


def register_resources(mcp: FastMCP):
    """Registers MCP resources"""
    
    @mcp.resource("file:///data/seasons_guide.txt", mime_type="text/plain")
    async def read_seasons_guide() -> str:
        """Reads the travel seasons guide file."""
        try:
            data_dir = Path(__file__).parent.parent.parent.parent / "data"
            file_path = data_dir / "seasons_guide.txt"
            async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
                content = await f.read()
            return content
        except FileNotFoundError:
            return "Seasons guide file not found."
        except (OSError, UnicodeDecodeError) as e:
            logger.error("Error reading seasons guide: %s", str(e))
            return "Error loading seasons data."
    
    @mcp.resource("file:///data/documents_checklist.txt", mime_type="text/plain")
    async def read_documents_checklist() -> str:
        """Reads the travel documents checklist file."""
        try:
            data_dir = Path(__file__).parent.parent.parent.parent / "data"
            file_path = data_dir / "documents_checklist.txt"
            async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
                content = await f.read()
            return content
        except FileNotFoundError:
            return "Documents checklist file not found."
        except (OSError, UnicodeDecodeError) as e:
            logger.error("Error reading documents checklist: %s", str(e))
            return "Error loading documents data."
