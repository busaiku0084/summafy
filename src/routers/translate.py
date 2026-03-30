from fastapi import APIRouter

from src.schemas import (
    LanguageInfo,
    LanguagesResponse,
    TranslateRequest,
    TranslateResponse,
)
from src.services.translation import translate

router = APIRouter(prefix="/translate", tags=["translate"])

SUPPORTED_LANGUAGES: list[LanguageInfo] = [
    LanguageInfo(code="en", name="English"),
    LanguageInfo(code="ja", name="Japanese"),
    LanguageInfo(code="zh", name="Chinese"),
    LanguageInfo(code="ko", name="Korean"),
    LanguageInfo(code="fr", name="French"),
    LanguageInfo(code="de", name="German"),
    LanguageInfo(code="es", name="Spanish"),
    LanguageInfo(code="pt", name="Portuguese"),
    LanguageInfo(code="it", name="Italian"),
    LanguageInfo(code="ru", name="Russian"),
    LanguageInfo(code="ar", name="Arabic"),
    LanguageInfo(code="hi", name="Hindi"),
    LanguageInfo(code="th", name="Thai"),
    LanguageInfo(code="vi", name="Vietnamese"),
    LanguageInfo(code="id", name="Indonesian"),
    LanguageInfo(code="nl", name="Dutch"),
    LanguageInfo(code="pl", name="Polish"),
    LanguageInfo(code="sv", name="Swedish"),
    LanguageInfo(code="tr", name="Turkish"),
]


@router.post("", response_model=TranslateResponse)
async def translate_text(req: TranslateRequest) -> TranslateResponse:
    result = await translate(
        text=req.text,
        target_lang=req.target_lang,
        source_lang=req.source_lang,
    )
    return TranslateResponse(
        translated_text=result.translated_text,
        source_lang=result.source_lang,
        target_lang=result.target_lang,
    )


@router.get("/languages", response_model=LanguagesResponse)
async def list_languages() -> LanguagesResponse:
    return LanguagesResponse(languages=SUPPORTED_LANGUAGES)
