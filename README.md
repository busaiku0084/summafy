# Summafy

テキスト翻訳マイクロサービス。MyMemory Translation API を利用した REST API。

## クイックスタート

### Docker（推奨）

```bash
docker compose up --build
```

http://localhost:8000 でサーバーが起動します。

### ローカル開発

```bash
python -m venv .venv
source .venv/bin/activate
pip install .[dev]
uvicorn src.main:app --reload
```

## API エンドポイント

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/health` | ヘルスチェック |
| POST | `/translate` | テキスト翻訳 |
| GET | `/translate/languages` | サポート言語一覧 |

### POST /translate

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, world!", "target_lang": "ja"}'
```

レスポンス:

```json
{
  "translated_text": "こんにちは、世界！",
  "source_lang": "auto",
  "target_lang": "ja"
}
```

`source_lang` を省略すると自動検出されます。明示的に指定することもできます:

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "target_lang": "fr"}'
```

### GET /translate/languages

```bash
curl http://localhost:8000/translate/languages
```

## 環境変数

| 変数 | デフォルト | 説明 |
|------|-----------|------|
| `SUMMAFY_MYMEMORY_API_URL` | `https://api.mymemory.translated.net/get` | 翻訳 API の URL |
| `SUMMAFY_TRANSLATION_TIMEOUT` | `10.0` | API タイムアウト（秒） |
| `SUMMAFY_LOG_LEVEL` | `info` | ログレベル |

## 開発

```bash
# リント
ruff check .
ruff format --check .

# 型チェック
mypy src/

# テスト
pytest -v

# フォーマット
ruff format .
```

## 技術スタック

- Python 3.12+
- FastAPI / Uvicorn
- MyMemory Translation API
- Docker / Docker Compose
- Ruff（リンター/フォーマッター）+ mypy（型チェック）
- GitHub Actions CI
