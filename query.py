from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import Chroma
from ddgs import DDGS
import requests
from datetime import datetime

DB_PATH = "chroma_db"

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
llm = OllamaLLM(model="llama3.2", num_predict=250)

WEB_TRIGGER_WORDS = ["today", "current", "latest", "news", "now", "recent", "price", "score"]
TIME_TRIGGER_WORDS = ["time", "date", "day is it", "today's date"]


def needs_web_search(query: str) -> bool:
    q = query.lower()
    return any(word in q for word in WEB_TRIGGER_WORDS)


def needs_time_lookup(query: str) -> bool:
    q = query.lower()
    return any(word in q for word in TIME_TRIGGER_WORDS)


def get_real_time_info():
    """Fetch real current date & time directly from an internet time API."""
    try:
        res = requests.get("https://worldtimeapi.org/api/timezone/Asia/Kolkata", timeout=5)
        data = res.json()
        dt = datetime.fromisoformat(data["datetime"])
        formatted = dt.strftime("%A, %d %B %Y, %I:%M %p (India time)")
        return formatted
    except Exception as e:
        # Fallback to system time if internet API fails
        return datetime.now().strftime("%A, %d %B %Y, %I:%M %p")


def web_search(query: str, max_results: int = 4):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return ""
        return "\n\n".join([f"{r['title']}: {r['body']}" for r in results])
    except Exception as e:
        print(f"[web search error: {e}]")
        return ""


def answer(query: str):
    # Case 1: Direct real-time date/time question -> use internet time API, skip LLM guessing
    if needs_time_lookup(query):
        real_time = get_real_time_info()
        return f"The current date and time is: {real_time}", []

    # Case 2: Other live info -> web search
    docs = vectorstore.similarity_search(query, k=2)
    doc_context = "\n\n".join([doc.page_content for doc in docs])

    web_context = ""
    if needs_web_search(query):
        web_context = web_search(query)

    if web_context:
        prompt = f"""You are a helpful assistant with access to live web search results below. These results ARE the current, real information — trust them completely, do not say you're unsure or that your training data is outdated.

Web Search Results:
{web_context}

Question: {query}

Instructions:
- Extract the actual answer directly from the Web Search Results above.
- Answer confidently and directly. Do NOT say "I'm not sure" or mention training data cutoffs.
- Keep the answer short and to the point. Do not mention sources, links, or websites in your answer.

Answer:"""
    else:
        prompt = f"""You are a helpful assistant. Answer the question directly and clearly.

Document Context:
{doc_context}

Question: {query}

Instructions:
- If Document Context is relevant, use it.
- Otherwise, answer using your own general knowledge.
- Give a clear, direct answer. Never say you don't have information.

Answer:"""

    response = llm.invoke(prompt)
    return response, []


if __name__ == "__main__":
    print("RAG Chatbot ready! Type 'exit' to quit.\n")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        resp, sources = answer(query)
        print(f"\nBot: {resp}\n")