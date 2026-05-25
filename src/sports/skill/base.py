from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from ..config import settings
from playwright.async_api import async_playwright
import asyncio

class BettingSiteScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    async def init(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.page = await self.browser.new_page()

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
