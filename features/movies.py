import requests, unicodedata, config

from config import Style

def get_movies_in_theatres():
    trending_movies = []
    res = requests.get(f"https://api.themoviedb.org/3/movie/now_playing?api_key={config.MOVIE_DB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(unicodedata.normalize("NFKD",str(f'{Style.YELLOW}{r["original_title"]}{Style.RESET}\n{r["overview"]}\n')))
    return '\n'.join(map(str, trending_movies[:10]))

def get_trending_movies():
    trending_movies = []
    res = requests.get(f"https://api.themoviedb.org/3/trending/movie/week?api_key={config.MOVIE_DB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(unicodedata.normalize("NFKD",str(f'{Style.YELLOW}{r["original_title"]}{Style.RESET}\n{r["overview"]}\n')))
    return '\n'.join(map(str, trending_movies[:10]))

def get_popular_movies():
    trending_movies = []
    res = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={config.MOVIE_DB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(unicodedata.normalize("NFKD",str(f'{Style.YELLOW}{r["original_title"]}{Style.RESET}\n{r["overview"]}\n')))
    return '\n'.join(map(str, trending_movies[:10]))