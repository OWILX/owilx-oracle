from .scraper import SportScraper 

scraper = SportScraper(sport="basketball", headless=False)
await scraper.start()
data = await scraper.extract_data()
print(data["html"][:500])
await scraper.close()
