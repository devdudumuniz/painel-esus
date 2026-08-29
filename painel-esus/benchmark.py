import asyncio
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.data.use_cases.create_bases.create_cache import CreateCacheUseCase

class MockSession:
    def get(self, url):
        class MockResponse:
            def __init__(self, status):
                self.status = status
            async def __aenter__(self):
                await asyncio.sleep(0.001)
                return self
            async def __aexit__(self, exc_type, exc_val, exc_tb):
                pass
            def text(self):
                return "Mock text"
        return MockResponse(200)

async def run_benchmark():
    use_case = CreateCacheUseCase()
    session = MockSession()

    # 20,000 URLs to simulate a large load
    urls = [f"http://example.com/api/data/{i}" for i in range(20000)]

    print(f"Starting baseline benchmark with {len(urls)} URLs...")
    start_time = time.time()
    await use_case._get_all(session, urls)
    end_time = time.time()

    print(f"Baseline time taken for {len(urls)} URLs: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
