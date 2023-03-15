import fcntl
import logging

logger = logging.getLogger(__name__)


class CustomLock:
    def __init__(self, lock_file: str) -> None:
        self.lock = open(lock_file, 'w')
        super().__init__()

    def close(self) -> None:
        self.release_lock()
        self.lock.close()

    def acquire_lock(self) -> None:
        fcntl.flock(self.lock, fcntl.LOCK_EX)

    def release_lock(self) -> None:
        fcntl.flock(self.lock, fcntl.LOCK_EX)

    def __enter__(self) -> 'CustomLock':
        self.acquire_lock()
        return self

    def __exit__(self, exc_type=None, exc_value=None, traceback=None) -> None:
        if exc_type:
            logger.error(exc_value, exc_info=traceback)
        self.close()
