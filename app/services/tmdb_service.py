import requests
from flask import current_app


def get_popular_movies(page=1):
    """Lấy danh sách phim phổ biến từ TMDB."""
    api_key = current_app.config["MOVIES_API_KEY"]
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&page={page}"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        return data.get("results", []), data.get("total_pages", 1)
    except requests.RequestException:
        return [], 1


def get_movie_detail(movie_id):
    """Lấy chi tiết 1 phim từ TMDB."""
    api_key = current_app.config["MOVIES_API_KEY"]
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.RequestException:
        return None

def search_movies(query, page=1):
    api_key = current_app.config["MOVIES_API_KEY"]
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": query,
        "page": page,
        "include_adult": False
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        return data.get("results",[]), data.get("total_pages",1)
    except requests.RequestException:
        return [], 1