import  requests, datetime, unicodedata, config

from config import Style

def get_latest_news():
    news = []
    res = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&language=en&apiKey={config.NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        if "ESPN" not in article["title"]:
            news.append(unicodedata.normalize("NFKD", str(f'{Style.YELLOW}{str(article["title"])}{Style.RESET}\n{str(article["description"])}\n')))
    return '\n'.join(map(str, news[:5]))

def get_latest_science_news():
    news = []
    res = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&language=en&apiKey={config.NEWS_API_KEY}&category=science").json()
    articles = res["articles"]
    for article in articles:
        if "pictures" not in article["title"] and "space radiation" not in article["title"]:
            news.append(unicodedata.normalize("NFKD", str(f'{Style.YELLOW}{article["title"]}{Style.RESET}\n{article["description"]}\n')))
    return '\n'.join(map(str, news[:5]))

def get_latest_tech_news():
    news = []
    res = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&language=en&apiKey={config.NEWS_API_KEY}&category=technology").json()
    articles = res["articles"]
    for article in articles:
        if "Steam" and "Summer Sale" not in article["title"]:
            news.append(unicodedata.normalize("NFKD", str(f'{Style.YELLOW}{article["title"]}{Style.RESET}\n{article["description"]}\n')))
    return '\n'.join(map(str, news[:5]))

def get_space_news():
    news = []
    today = str(datetime.datetime.today())
    today = today.split(' ')[0]
    url = (f'https://newsapi.org/v2/everything?q=SpaceX&from={today}&sortBy=relevancy&language=en&apiKey={config.NEWS_API_KEY}')
    response = requests.get(url).json()
    articles = response["articles"]
    for article in articles:
        if "Twitter" not in article["title"] and "Photographer" not in article["title"] and "ISRO" not in article["title"]:
            if "Billionaires" not in article["content"]:
                if "TechScape" not in article["title"]:
                    news.append(unicodedata.normalize("NFKD", str(f'{Style.YELLOW}{str(article["title"])}{Style.RESET}\n{str(article["description"])}\n')))
    return '\n'.join(map(str, news[:5]))