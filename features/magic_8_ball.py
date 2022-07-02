import random

def Magic_8_Ball(query):
    answers = ["It is certain", "As I see it, Yes", "Reply Hazy, Try Again", "Don't count on it",
               "It is decidedly so", "Most Likely", "Ask again later", "My reply is, No",
               "Without a doubt", "Outlook Good", "Wait and see", "My sources say No",
               "Definitely", "Yes", "Can not predict now", "Outlook not so good",
               "You may rely on it", "Signs point to yes", "Concentrate and ask again", "Very doubtful"]
    if "should" in query or "will" in query or "could" in query or "can" in query:
        return f"{answers[random.randint(0, len(answers) - 1)]}"
    elif "should" not in query or "will" not in query or "could" not in query or "can" not in query:
        return "I don't understand, please respond with a yes or no question"
