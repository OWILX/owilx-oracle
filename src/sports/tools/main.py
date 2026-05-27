from . import fixture

# Initialize the tool
daily_fixture_tool = fixture.DailyFixtureTool()

# Use the tool
games = await daily_fixture_tool.get_todays_games("soccer")
print(games)
