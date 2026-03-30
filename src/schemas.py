from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to translate")
    source_lang: str | None = Field(
        default=None,
        description="Source language code (e.g. 'en'). Auto-detect if omitted.",
    )
    target_lang: str = Field(..., description="Target language code (e.g. 'ja')")


class TranslateResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str


class LanguageInfo(BaseModel):
    code: str
    name: str


class LanguagesResponse(BaseModel):
    languages: list[LanguageInfo]
