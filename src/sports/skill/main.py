import asyncio
from .scraper import SportScraper 

async def main():
    scraper = SportScraper(sport="basketball", headless=False)
    await scraper.start()
    data = await scraper.extract_data()
    print(data["html"][:500])
    await scraper.close()

if __name__ == "__main__":
    await main()