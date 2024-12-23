# BotAInik
Бот для подготовки к собеседованиям

## Данные

База знаний состоит из ML хэндбука яндекса, лекций Соколова, а также десятков других книг и статей про Data Science, Machine Learning и AI.

## Техническое описание

Данные разбиваются на чанки по 300 слов с перекрытием в 50 слов.

Далее мы генерируем с помощью LLM опорные фразы к каждому чанку по убыванию релевантости опорника. Например, если в чанке говорится о машинном обучении и затрагивается линейная регрессия, то опорники будут:
1) Что такое машинное обучение?
2) Линейная регрессия

Теперь у нас есть чанк, опорники и их важность. Кладем это все в Chroma, после чего сравниваем запрос пользователя с опорниками, учитывая важность опорника в формуле. В контекст подаем самые релевантные чанки, получаем ответ.

- **Эмбеддер**: all-MiniLM-L6-v2
- **База данных**: CHROMA
- **LLM**: Mistral Large
- **Other**: FastAPI, JavaScript, HTML, CSS


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

