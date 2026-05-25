import asyncio
from .scraper import SportScraper 

async def main():
    scraper = SportScraper(sport="basketball", headless=True)
    await scraper.start()
    data = await scraper.extract_data()
    #print(f"Extracted {len(data['structured_data'])} matches")
    with open("filtered_content.html", "w") as f:
        f.write(data["html"])
    await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())
