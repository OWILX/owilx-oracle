#from . import fixture

# Initialize the tool
#daily_fixture_tool = fixture.DailyFixtureTool()

# Use the tool
#games = await daily_fixture_tool.get_todays_games("soccer")
#print(games)

import asyncio
from src.sports.tools.fixture import DailyFixtureTool

async def main():
    # Instantiate the tool
    daily_fixture_tool = DailyFixtureTool()
    
    # Use await inside this async function
    games = await daily_fixture_tool.get_todays_games("soccer")
    print(games)

if __name__ == "__main__":
    # This is the entry point that runs the async function
    asyncio.run(main())
