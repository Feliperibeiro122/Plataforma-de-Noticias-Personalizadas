import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news_by_preferences(preferences: str):
    #Se o usuário não tiver preferências, então será buscado algo mais amplo
    query = preferences if preferences else "tecnologia"

    #URL montada com parâmetros
    params = {
        "q": query,
        "apikey": API_KEY,
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": 10
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("articles", [])
    else:
        #Se der erro na API externa, retorna uma lista vazia
        return[]