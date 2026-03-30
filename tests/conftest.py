from collections.abc import Iterator
from unittest.mock import AsyncMock, patch

import pytest

from src.services.translation import TranslationResult


def _make_mock(
    return_value: TranslationResult | None = None,
    side_effect: Exception | None = None,
) -> AsyncMock:
    mock = AsyncMock()
    if side_effect:
        mock.side_effect = side_effect
    else:
        mock.return_value = return_value or TranslationResult(
            translated_text="こんにちは",
            source_lang="auto",
            target_lang="ja",
        )
    return mock


@pytest.fixture()
def mock_translate_success() -> Iterator[AsyncMock]:
    with patch(
        "src.routers.translate.translate", new_callable=AsyncMock
    ) as m:
        m.return_value = TranslationResult(
            translated_text="こんにちは",
            source_lang="auto",
            target_lang="ja",
        )
        yield m


@pytest.fixture()
def mock_translate_timeout() -> Iterator[AsyncMock]:
    from src.exceptions import TranslationTimeoutError

    with patch(
        "src.routers.translate.translate", new_callable=AsyncMock
    ) as m:
        m.side_effect = TranslationTimeoutError("Translation API timed out")
        yield m


@pytest.fixture()
def mock_translate_error() -> Iterator[AsyncMock]:
    from src.exceptions import ExternalAPIError

    with patch(
        "src.routers.translate.translate", new_callable=AsyncMock
    ) as m:
        m.side_effect = ExternalAPIError("Translation API returned 500")
        yield m
