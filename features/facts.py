import requests, json, randfacts, random

def get_random_fact():
    random_fact = randfacts.get_fact(False)
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    res = requests.get(url)
    data = json.loads(res.text)
    useless_fact = data["text"]
    fact = random.randint(0, 1)
    if fact == 0:
        return random_fact
    elif  fact == 1:
        return useless_fact