from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class SiteScraper(ABC):
    """Abstract base class for site scrapers."""

    @abstractmethod
    async def start(self):
        """Initialize the browser and playwright context."""
        pass

    @abstractmethod
    async def navigate_to_site(self, url: str):
        """Navigate to the given URL."""
        pass

    @abstractmethod
    async def extract_data(self, url: Optional[str] = None) -> Dict:
        """
        Extract data from the current page or the provided URL.
        Should handle scrolling to load dynamic content and return structured data.
        """
        pass

    @abstractmethod
    async def close(self):
        """Clean up browser and playwright resources."""
        pass