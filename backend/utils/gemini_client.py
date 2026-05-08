import time
from typing import Any, Callable
from backend.utils.logger import app_logger

class GeminiAPIError(Exception):
    """Custom exception for Gemini API failures."""
    pass

def call_gemini_with_retry(
    api_func: Callable,
    *args,
    max_retries: int = 3,
    base_delay: float = 2.0,
    **kwargs
) -> Any:
    """
    Lightweight resilient wrapper for Gemini API calls.
    Implements retries with exponential backoff and graceful error handling.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            # Here api_func would be the actual Gemini generation call
            return api_func(*args, **kwargs)

        except Exception as e:
            attempt += 1
            error_msg = str(e)

            app_logger.warning(
                f"Gemini API call failed (attempt {attempt}/{max_retries}): {error_msg}"
            )

            if attempt >= max_retries:
                app_logger.error(f"Gemini API call exhausted all retries. Final error: {error_msg}")
                raise GeminiAPIError(f"Failed to communicate with Gemini API: {error_msg}") from e

            # Exponential backoff
            sleep_time = base_delay * (2 ** (attempt - 1))
            time.sleep(sleep_time)
