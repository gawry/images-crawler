import threading
import pytest
from images_crawler.services import DownloadLimiter


@pytest.fixture(autouse=True)
def limiter():
    # move this to the root conftest.py file
    DownloadLimiter._instance = None
    return DownloadLimiter  

def test_download_limiter_increment(limiter):
    limiter = limiter(max_downloads=5)
    assert limiter.downloads == 0

    limiter.increment()
    assert limiter.downloads == 1

    limiter.increment()
    assert limiter.downloads == 2

def test_download_limiter_is_limit_reached(limiter):
    limiter = limiter(max_downloads=3)
    assert not limiter.is_limit_reached()
    assert limiter.downloads == 0
    
    limiter.increment()
    assert limiter.downloads == 1
    assert not limiter.is_limit_reached()

    limiter.increment()
    assert limiter.downloads == 2
    assert not limiter.is_limit_reached()

    limiter.increment()
    assert limiter.downloads == 3
    assert limiter.is_limit_reached()

def test_download_limiter_singleton(limiter):
    limiter1 = limiter(max_downloads=5)
    limiter2 = limiter(max_downloads=10)

    assert limiter1 is limiter2

def test_download_limiter_thread_safety(limiter):
    def increment_downloads(limiter):
        for _ in range(1000):
            limiter.increment()

    limiter = limiter(max_downloads=1000)

    threads = []
    for _ in range(10):
        thread = threading.Thread(target=increment_downloads, args=(limiter,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    assert limiter.downloads == 10000