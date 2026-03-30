from dataclasses import dataclass

import httpx

from src.config import Settings, get_settings
from src.exceptions import ExternalAPIError, TranslationTimeoutError


@dataclass(frozen=True)
class TranslationResult:
    translated_text: str
    source_lang: str
    target_lang: str


async def translate(
    text: str,
    target_lang: str,
    source_lang: str | None = None,
    settings: Settings | None = None,
) -> TranslationResult:
    """Translate text using MyMemory API."""
    cfg = settings or get_settings()
    src = source_lang or "autodetect"
    langpair = f"{src}|{target_lang}"

    try:
        async with httpx.AsyncClient(
            timeout=cfg.translation_timeout,
        ) as client:
            resp = await client.get(
                cfg.mymemory_api_url,
                params={"q": text, "langpair": langpair},
            )
            resp.raise_for_status()
    except httpx.TimeoutException as e:
        raise TranslationTimeoutError("Translation API timed out") from e
    except httpx.HTTPStatusError as e:
        raise ExternalAPIError(
            f"Translation API returned {e.response.status_code}"
        ) from e
    except httpx.HTTPError as e:
        raise ExternalAPIError(f"Translation API request failed: {e}") from e

    data: dict[str, object] = resp.json()
    response_data = data["responseData"]
    if not isinstance(response_data, dict):
        raise ExternalAPIError("Unexpected API response format")
    translated = str(response_data["translatedText"])

    return TranslationResult(
        translated_text=translated,
        source_lang=source_lang or "auto",
        target_lang=target_lang,
    )
