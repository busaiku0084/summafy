class TranslationError(Exception):
    """Base exception for translation errors."""


class ExternalAPIError(TranslationError):
    """External translation API returned an error."""


class TranslationTimeoutError(TranslationError):
    """External translation API timed out."""
