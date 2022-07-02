import requests, datetime
from bs4 import BeautifulSoup

def get_horoscope(query):
    if "aries" in query:
        zodiac_sign = "1"
    elif "aquarius" in query:
        zodiac_sign = "11"
    elif "cancer" in query:
        zodiac_sign = "4"
    elif "capricorn" in query:
        zodiac_sign = "10"
    elif "gemini" in query or "my horoscope" in query:
        zodiac_sign = "3"
    elif "leo" in query:
        zodiac_sign = "5"
    elif "libra" in query:
        zodiac_sign = "7"
    elif "pisces" in query:
        zodiac_sign = "12"
    elif "sagittarius" in query:
        zodiac_sign = "9"
    elif "scorpio" in query:
        zodiac_sign = "8"
    elif "taurus" in query:
        zodiac_sign = "2"
    elif "virgo" in query:
        zodiac_sign = "6"
    else:
        print("Please enter a valid star sign")
    res = requests.get(f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={zodiac_sign}")
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find('div', attrs={'class': 'main-horoscope'})
    year = datetime.datetime.today().year
    return str(data.p.text).split(f"{year} - ")[1]