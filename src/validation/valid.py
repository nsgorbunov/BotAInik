import getpass
import os
import requests
import time
import threading
from functools import wraps
from langchain import hub
from langsmith.evaluation import evaluate
from langchain_mistralai import ChatMistralAI
from src.rag_pipeline.rag_chain import RAGChain

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGCHAIN_PROJECT'] = 'BotAInik'
os.environ["LANGCHAIN_API_KEY"] = "---"
os.environ["MISTRAL_API_KEY"] = "---"

# Глобальный RateLimiter
class RateLimiter:
    def __init__(self, min_interval):
        self.min_interval = min_interval
        self.lock = threading.Lock()
        self.last_call = 0

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            with self.lock:
                now = time.time()
                elapsed = now - self.last_call
                wait_time = self.min_interval - elapsed
                if wait_time > 0:
                    print(f"Ожидание {wait_time:.2f} секунд перед вызовом {func.__name__}")
                    time.sleep(wait_time)
                result = func(*args, **kwargs)
                self.last_call = time.time()
                return result
        return wrapped

# Экземпляр RateLimiter с задержкой 10 секунд
rate_limiter = RateLimiter(10)

# Декоратор для повторных попыток при ошибке 429
def retry_on_429(max_retries=5, backoff_factor=2):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            retries = 0
            delay = 1
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        print(f"Получен 429. Повторная попытка через {delay} секунд...")
                        time.sleep(delay)
                        retries += 1
                        delay *= backoff_factor
                    else:
                        raise
            print(f"Максимальное количество попыток достигнуто для функции {func.__name__}")
            return None
        return wrapped
    return decorator

def safe_invoke(invoker, **kwargs):
    @rate_limiter
    @retry_on_429()
    def wrapped():
        response = invoker(**kwargs)
        if response is None:
            raise Exception("Не удалось получить ответ после нескольких попыток.")
        return response
    return wrapped()

eval_llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
)

grade_prompt_answer_accuracy = hub.pull("langchain-ai/rag-answer-vs-reference")
grade_prompt_answer_helpfulness = hub.pull("langchain-ai/rag-answer-helpfulness")
grade_prompt_hallucinations = hub.pull("langchain-ai/rag-answer-hallucination")
grade_prompt_doc_relevance = hub.pull("langchain-ai/rag-document-relevance")

rag_chain = RAGChain()

def answer_evaluator(run, example) -> dict:
    input_question = example.inputs["question"]
    reference = example.outputs["ground_truth"]
    prediction = run.outputs["answer"]

    llm = eval_llm
    answer_grader = grade_prompt_answer_accuracy | llm

    try:
        print(f"Вызов MistralAI для оценки ответа на вопрос: {input_question}")
        score_response = safe_invoke(
            lambda: answer_grader.invoke({
                "question": input_question,
                "correct_answer": reference,
                "student_answer": prediction
            })
        )
        if score_response is None:
            score = 0
        else:
            score = score_response.get("Score", 0)
            print(f"Получен скор: {score}")
    except Exception as e:
        print(f"Ошибка при вызове MistralAI: {e}")
        score = 0

    return {"key": "answer_v_reference_score", "score": score}

# Обертка для вызова RAGChain.validate с задержкой и повторными попытками
def delayed_rag_validate(question):
    try:
        print(f"Вызов RAGChain.validate для вопроса: {question}")
        response = safe_invoke(lambda: rag_chain.validate(question))
        if response is None:
            response = {"answer": "Ошибка при получении ответа."}
        print(f"Получен ответ от RAGChain.validate")
    except Exception as e:
        print(f"Ошибка при вызове RAGChain.validate: {e}")
        response = {"answer": "Ошибка при получении ответа."}

    return response

# Функция для оценки набора данных
def evaluate_dataset_with_langsmith(dataset_name, grade_prompt_name):
    experiment_results = evaluate(
        lambda inputs: delayed_rag_validate(inputs["question"]),
        data=dataset_name,
        evaluators=[answer_evaluator],
        experiment_prefix=grade_prompt_name,
    )
    return experiment_results

# Функция для получения среднего балла
def get_average_score(experiment_results):
    results = experiment_results.to_pandas()
    mean = results['feedback.answer_v_reference_score'].mean()
    return mean

# Оценка точности ответа
dataset_name = 'Validation_data'
grade_prompt_name = "rag-answer-vs-reference"

experiment_results = evaluate_dataset_with_langsmith(dataset_name, grade_prompt_name)
average_score = get_average_score(experiment_results)

print(f"Усредненная оценка: {average_score}")