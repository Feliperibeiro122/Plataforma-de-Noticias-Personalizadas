import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news_by_preferences(termo: str, page: int = 1, size:int = 10):
    #Se o usuário não tiver preferências, então será buscado algo mais amplo
    query = termo if termo else "tecnologia"

    #URL montada com parâmetros
    params = {
        "q": query,
        "apiKey": API_KEY,
        "language": "pt",
        "sortBy": "publishedAt",
        "page": page,
        "pageSize": size
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("articles", [])
        return []
    except Exception as e:
        print(f"Erro na NewsAPI: {e}")
        return []