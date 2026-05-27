import httpx
from datetime import date
from typing import Dict, Literal
from ..config import settings

class DailyFixtureTool:
    def __init__(self):
        self.api_key = settings.SPORTRADAR_API_KEY
        self.base_url = "https://api.sportradar.com"

    async def get_todays_games(self, sport: Literal["soccer", "basketball", "baseball", "americanFootball"] = "soccer") -> Dict:
        """Get today's games for a specific sport"""
        # Map sports to their API paths
        sport_paths = {
            "soccer": "soccer/league/v4",
            "basketball": "basketball/nba/trial/v7",
            "baseball": "baseball/mlb/trial/v7", 
            "americanFootball": "american-football/nfl/trial/v7"
        }

        if sport not in sport_paths:
            raise ValueError(f"Unsupported sport: {sport}")

        # Format today's date as YYYY-MM-DD
        today = date.today().strftime('%Y-%m-%d')

        # Build the correct API endpoint
        url = f"{self.base_url}/{sport_paths[sport]}/schedules/{today}/schedule.json"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={"api_key": self.api_key}
            )
            response.raise_for_status()
            return response.json()
