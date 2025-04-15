import json
import os
import aiohttp
from bs4 import BeautifulSoup
from typing import List

class BaseRetriever:
    async def fetch_page(self, session, url: str) -> str:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return ""

class BaseExtractor:
    def extract_links(self, html: str) -> list:
        soup = BeautifulSoup(html, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True)]

class BaseArchiver:
    def __init__(self, output_dir="archives"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def archive_data(self, data: dict, filename: str):
        filepath = os.path.join(self.output_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Failed to archive data to {filepath}: {e}")