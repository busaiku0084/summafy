from dataclasses import dataclass

import httpx

from src.config import Settings, get_settings


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

    async with httpx.AsyncClient(timeout=cfg.translation_timeout) as client:
        resp = await client.get(
            cfg.mymemory_api_url,
            params={"q": text, "langpair": langpair},
        )
        resp.raise_for_status()

    data = resp.json()
    response_data: dict[str, str] = data["responseData"]
    translated = response_data["translatedText"]

    return TranslationResult(
        translated_text=translated,
        source_lang=source_lang or "auto",
        target_lang=target_lang,
    )
