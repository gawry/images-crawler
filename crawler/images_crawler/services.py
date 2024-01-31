import threading


class DownloadLimiter:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DownloadLimiter, cls).__new__(cls)
                cls._instance.__initialized = False
        return cls._instance

    def __init__(self, max_downloads: int):
        if self.__initialized: 
            return
        self.max_downloads = max_downloads
        self.downloads = 0
        self.lock = threading.Lock()
        self.__initialized = True

    def increment(self):
        with self.lock:
            self.downloads += 1

    def is_limit_reached(self):
        with self.lock:
            return self.downloads >= self.max_downloads