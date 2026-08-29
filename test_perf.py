import asyncio
import time
import aiohttp
from unittest.mock import AsyncMock

class MockCreateCacheUseCase:
    async def _get_page(self, session, url):
        await asyncio.sleep(0.001)
        return url

    async def _get_all_original(self, session, urls):
        tasks = []
        for url in urls:
            task = asyncio.create_task(self._get_page(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results

    async def _get_all_chunked(self, session, urls):
        results = []
        chunk_size = 500
        for i in range(0, len(urls), chunk_size):
            chunk = urls[i:i + chunk_size]
            tasks = [asyncio.create_task(self._get_page(session, url)) for url in chunk]
            res = await asyncio.gather(*tasks)
            results.extend(res)
        return results

async def main():
    use_case = MockCreateCacheUseCase()
    urls = [f"http://example.com/{i}" for i in range(20000)]

    start = time.time()
    await use_case._get_all_original(None, urls)
    print("Original:", time.time() - start)

    start = time.time()
    await use_case._get_all_chunked(None, urls)
    print("Chunked:", time.time() - start)

asyncio.run(main())
