import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.rag_pipeline.rag_chain import RAGChain

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "---"
os.environ["LANGCHAIN_PROJECT"] = "BotAInik"

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

class UserQuery(BaseModel):
    question: str

@app.post("/api/ask")
async def ask_question(payload: UserQuery):
    question = payload.question.strip()
    if not question:
        return JSONResponse(
            status_code=400,
            content={"error": "Пустой запрос"}
        )

    rag_chain = RAGChain()
    answer = rag_chain.run(question)
    return {"answer": answer}

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join("frontend", "index.html"))
