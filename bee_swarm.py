import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup
from worker_jobs.worker_bees import BaseRetriever, BaseExtractor, BaseArchiver

class Bee:
    def __init__(self, url: str, retriever: BaseRetriever, extractor: BaseExtractor, archiver: BaseArchiver, index: int):
        self.url = url
        self.retriever = retriever
        self.extractor = extractor
        self.archiver = archiver
        self.links = []
        self.index = index 

    async def process(self, session) -> dict:
        html = await self.retriever.fetch_page(session, self.url)
        if html:
            self.links = self.extractor.extract_links(html)
        else:
            print(f"Failed to fetch: {self.url}")
        
        data = {
            "url": self.url,
            "content_preview": html[:200] if html else "",
            "links": self.links
        }
        # Generate a unique filename for this bee's output.
        filename = f"bee_{self.index}.json"
        self.archiver.archive_data(data, filename)
        
        return data

async def main():
    url = "https://en.wikipedia.org/wiki/Model_Context_Protocol"
    
    # Create shared instances of retriever and extractor
    retriever = BaseRetriever()
    extractor = BaseExtractor()
    archiver = BaseArchiver(output_dir="archives")

    # Create a list of 500 bees; they all use the same URL (for testing purposes)
    bees = [Bee(url, retriever, extractor, archiver, index=i) for i in range(500)]
    start = time.perf_counter()
    
    async with aiohttp.ClientSession() as session:
        # Create tasks for all bees to process the page concurrently
        tasks = [bee.process(session) for bee in bees]
        results = await asyncio.gather(*tasks)
    
    duration = time.perf_counter() - start
    print(f"Finished in {duration:.2f} seconds with {len(bees)} bees.")

if __name__ == "__main__":
    asyncio.run(main())