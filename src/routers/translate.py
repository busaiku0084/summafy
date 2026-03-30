from fastapi import APIRouter

from src.schemas import TranslateRequest, TranslateResponse

router = APIRouter(prefix="/translate", tags=["translate"])


@router.post("", response_model=TranslateResponse)
async def translate_text(req: TranslateRequest) -> TranslateResponse:
    # TODO: implement actual translation logic
    return TranslateResponse(
        translated_text=req.text,
        source_lang=req.source_lang or "auto",
        target_lang=req.target_lang,
    )
