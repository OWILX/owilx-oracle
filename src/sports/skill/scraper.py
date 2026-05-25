import asyncio
import os
import json
import openai
from typing import Dict, List, Literal, Optional
from playwright.async_api import async_playwright
from .base import SiteScraper

Sport = Literal["basketball", "football", "americanFootball", "baseball"]


class SportScraper(SiteScraper):
    def __init__(self, sport: Sport, headless: bool = True):
        self.sport = sport
        self.headless = headless
        self.browser = None
        self.page = None
        self.context = None
        self.playwright = None

    async def start(self):
        """Launch browser with mobile device emulation (iPhone 13)."""
        self.playwright = await async_playwright().start()
        iphone = self.playwright.devices.get('iPhone 13')
        if iphone is None:
            iphone = {"viewport": {"width": 390, "height": 844}}
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(**iphone,
        geolocation={
            "latitude": 6.5244,
            "longitude": 3.3792
        },
        permissions=["geolocation"],
        locale="en-US",
        timezone_id="Africa/Lagos")
        
        self.page = await self.context.new_page()
        
        # Block unnecessary resources (images, fonts, CSS, etc.) to speed up loading
        await self.page.route("**/*.{png,jpg,jpeg,gif,svg,webp,ico,css,woff,woff2,ttf,otf,eot,map}", self._abort_route)
        # Optionally also block analytics and tracking scripts (adjust as needed)
        await self.page.route("**/gtm.js", self._abort_route)
        await self.page.route("**/gtag/js*", self._abort_route)
        await self.page.route("**/analytics*", self._abort_route)
        await self.page.route("**/fullstory*", self._abort_route)

    async def _abort_route(self, route):
        """Abort requests for blocked resources."""
        await route.abort()

    async def navigate_to_site(self, url: str):
        """Go to the specified URL."""
        if self.page:
            await self.page.goto(url, wait_until="networkidle")

    async def extract_data(self, url: Optional[str] = None) -> Dict:
        """Load the page, scroll to load all content, then extract data."""
        if url is None:
            url = f"https://www.football.com/ng/m/sport/{self.sport}/today/"

        await self.navigate_to_site(url)
        await asyncio.sleep(2)

        # Scroll to load all dynamic content
        last_height = 0
        for _ in range(30):  # safety limit
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1.8)
            
            new_height = await self.page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                await asyncio.sleep(2)  # final wait for any last content
                break
            last_height = new_height

                # Extract only the main content div with class "page-content page-content--ng"
        #content_html = await self.page.evaluate("""
        #    () => {
        #        const contentDiv = document.querySelector('.page-content.page-content--ng');
        #        return contentDiv ? contentDiv.outerHTML : '';
        #    }
        #""")
        content_html = await self.page.content()
        if not content_html:
            # Fallback: take the whole page content if the specific div isn't found
            content_html = await self.page.content()
            print("Warning: could not find .page-content.page-content--ng, using full HTML.")


        # Send HTML to the LLM for structured extraction
        #structured_data = await self._call_llm_for_extraction(content_html)
        
        return {
            "html": content_html,
            "url": url,
            #"structured_data": structured_data
        }

    async def _call_llm_for_extraction(self, html: str) -> List[Dict]:
        """
        Call OpenAI API (or compatible endpoint) to extract structured data from HTML.
        """
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            raise ValueError("LLM_API_KEY environment variable not set")
        
        base_url = os.getenv("LLM_URL")
        model = os.getenv("LLM_NAME")
        reasoning_effort = os.getenv("REASONING_EFFORT", "none")   # "none", "high", "max"
        client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)

        system_prompt = f"""
You are an expert at extracting sports betting data from HTML.

Extract all visible matches from the provided HTML into a clean JSON object with this exact structure:

{{
  "matches": [
    {{
      "home_team": "string",
      "away_team": "string",
      "time": "string",           // Format: "25, May 16:00"
      "league": "string",
      "odds": {{
        "home_win": float | null,
        "draw": float | null,
        "away_win": float | null
      }}
    }}
  ]
}}

Rules:
- Only extract matches that have at least home/away teams + some odds.
- For basketball, baseball, americanFootball → "draw" must be null.
- For football/soccer → "draw" is usually present.
- Use null for any missing odd.
- Be precise with team names (full names as shown).
- Detect the correct sport context from the page.
- If odds are in different formats (e.g. American +150), convert to decimal if possible, otherwise null.
- Return ONLY valid JSON. No explanations.
"""

        user_prompt = f"Extract matches and odds from this HTML:\n\n{html[:30000]}"

        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
                extra_body={"reasoning_effort": reasoning_effort}
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)
            
            if isinstance(parsed, dict) and "matches" in parsed:
                return parsed["matches"]
            elif isinstance(parsed, list):
                return parsed
            else:
                print("Unexpected JSON structure from LLM:", parsed)
                return []
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return []

    async def close(self):
        """Clean up resources."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()