import functools
import time
from typing import Callable, Optional, Tuple, Type

from nucleo import logger


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable] = None
):
    """
    Retry decorator that retries a function on specified exceptions.
    
    Args:
        max_attempts: Maximum number of attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Multiplier for delay after each retry (default: 2.0)
        exceptions: Tuple of exception types to catch (default: (Exception,))
        on_retry: Optional callback function called on each retry
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        logger.error(
                            f"Function {func.__name__} failed after "
                            f"{max_attempts} attempts: {e}"
                        )
                        raise
                    
                    logger.warning(
                        f"Function {func.__name__} failed on attempt "
                        f"{attempt}/{max_attempts}: {e}. "
                        f"Retrying in {current_delay}s..."
                    )
                    
                    if on_retry:
                        on_retry(attempt, e, current_delay)
                    
                    time.sleep(current_delay)
                    current_delay *= backoff

            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator