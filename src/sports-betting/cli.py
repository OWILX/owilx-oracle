import asyncio
import typer
from .data.ingestion import fetch_daily_fixtures

app = typer.Typer()

@app.command()
def fetch_fixtures():
    """Pull today's fixtures into Supabase."""
    asyncio.run(fetch_daily_fixtures())
    typer.echo("Fixtures updated.")


if __name__ == "__main__":
    app()
