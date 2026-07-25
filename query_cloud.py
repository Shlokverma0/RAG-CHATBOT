import os
import streamlit as st
from openai import OpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from ddgs import DDGS
import requests
from datetime import datetime

DB_PATH = "chroma_db"

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

WEB_TRIGGER_WORDS = ["today", "current", "latest", "news", "now", "recent", "price", "score"]
TIME_TRIGGER_WORDS = ["time", "date", "day is it", "today's date"]


def needs_web_search(query: str) -> bool:
    return any(word in query.lower() for word in WEB_TRIGGER_WORDS)


def needs_time_lookup(query: str) -> bool:
    return any(word in query.lower() for word in TIME_TRIGGER_WORDS)


def get_real_time_info():
    try:
        res = requests.get("https://worldtimeapi.org/api/timezone/Asia/Kolkata", timeout=5)
        data = res.json()
        dt = datetime.fromisoformat(data["datetime"])
        return dt.strftime("%A, %d %B %Y, %I:%M %p (India time)")
    except Exception:
        return datetime.now().strftime("%A, %d %B %Y, %I:%M %p")


def web_search(query: str, max_results: int = 4):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return ""
        return "\n\n".join([f"{r['title']}: {r['body']}" for r in results])
    except Exception:
        return ""


def answer(query: str):
    if needs_time_lookup(query):
        return f"The current date and time is: {get_real_time_info()}", []

    docs = vectorstore.similarity_search(query, k=2)
    doc_context = "\n\n".join([doc.page_content for doc in docs])

    web_context = web_search(query) if needs_web_search(query) else ""

    if web_context:
        system_prompt = "You are a helpful assistant with access to live web search results. Trust them completely, answer confidently, never mention training data cutoffs. Do not mention sources or links."
        user_prompt = f"Web Search Results:\n{web_context}\n\nQuestion: {query}\n\nAnswer directly using the results above."
    else:
        system_prompt = "You are a helpful assistant. Use the document context if relevant, otherwise use your own knowledge. Always give a direct, helpful answer."
        user_prompt = f"Document Context:\n{doc_context}\n\nQuestion: {query}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content, []