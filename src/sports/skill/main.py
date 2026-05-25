import asyncio
from .scraper import SportScraper 

async def main():
    scraper = SportScraper(sport="basketball", headless=True)
    await scraper.start()
    data = await scraper.extract_data()
    print(data["structured_data"])
    await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())