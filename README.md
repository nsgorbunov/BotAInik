# BotAInik
Бот для подготовки к собеседованиям

## Как запустить?
```
poetry install
poetry run pre-commit install
```

### Запуск бота
В config.yaml прописываем все настройки, прокидываем ключи к API
```
cd BotAInik
```
Сложите все PDF / TXT / DOCX файлы в одну папку docs/

Запустите:
```
poetry run python src/scripts/chunk_data.py --folder docs/ --output data/output.csv
```
Это создаст data/output.xlsx со столбцами text и meta.

Далее нужно сгенерировать опорники и их importance к каждому чанку:
```
poetry run python src/scripts/process_chunks.py --input data/output.csv --output data/chunks_with_phrases.csv
```

Теперь нужно загрузить данные в Chroma:
```
poetry run python src/scripts/ingest_data.py --csv data/chunks_with_phrases.csv --collection bota_inik
```
После того, как бд готова

Запускаем локально
```
poetry run uvicorn backend.app:app --reload --port 5000
```

