import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup

class Bee:
    def __init__(self, url):
        self.url = url
        self.links = []

    async def fetch_page(self, session):
        async with session.get(self.url) as response:
            if response.status == 200:
                html = await response.text()
                self.extract_links(html)

    def extract_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        self.links = [a['href'] for a in soup.find_all('a', href=True)]

async def main():
    url = "https://en.wikipedia.org/wiki/Model_Context_Protocol"
    bees = [Bee(url) for _ in range(500)]

    start = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [bee.fetch_page(session) for bee in bees]
        await asyncio.gather(*tasks)

    duration = time.perf_counter() - start
    print(f"✅ Finished in {duration:.2f} seconds with {len(bees)} bees.")

if __name__ == "__main__":
    asyncio.run(main())