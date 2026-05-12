import httpx
from datetime import date
from ..config import settings

async def fetch_daily_fixtures(league_id: int = None):
    """Fetch today's fixtures from API-Football and upsert into Supabase."""
    url = f"{settings.APIFOOTBALL_BASE_URL}/fixtures"
    params = {"date": date.today().isoformat()}
    if league_id:
        params["league"] = league_id

    headers = {"x-apisports-key": settings.APIFOOTBALL_KEY}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        fixtures = resp.json()["response"]
    
    for fix in fixtures:
        fixture = fix["fixture"]
        teams = fix["teams"]
        league = fix["league"]
        data = {
            "fixture_id": fixture["id"],
            "league_id": league["id"],
            "league_name": league["name"],
            "home_team": teams["home"]["name"],
            "away_team": teams["away"]["name"],
            "event_date": fixture["date"],
            "status": fixture["status"]["short"],
        }
        #supabase.table("fixtures").upsert(data).execute()
        print(data)
    return len(fixtures)