###########################################################
#------------------------ IMPORTS ------------------------#
###########################################################
import time, pyttsx3, speech_recognition, config

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from features import wiki, alarm, google_calendar, horoscope
from features import wolfram, magic_8_ball, date_time, facts
from features import currency_convert, jokes, advice, contact_list
from features import news, weather, movies, shopping_list
from features import todo_list, diary

from config import Style

###########################################################
#----------------------- VARIABLES -----------------------#
###########################################################
PATH = '../../webdrivers/chromedriver.exe'

###########################################################
#----------------------- FUNCTIONS -----------------------#
###########################################################
def get_voices():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    for voice in voices:
        print("Voice:")
        print("ID: %s" % voice.id)
        print("Name: %s" % voice.name)
        print("Age: %s" % voice.age)
        print("Gender: %s" % voice.gender)
        print("Languages Known: %s" % voice.languages)
        print("______________________________________")

def speak(audio):
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 145)
    engine.say(audio)
    engine.runAndWait()

def listen():
    recognize = speech_recognition.Recognizer()
    with speech_recognition.Microphone(device_index = 1) as source:
        recognize.adjust_for_ambient_noise(source, duration = 2)
        recognize.pause_threshold = 1
        audio = recognize.listen(source)
        query = ""
        try:
            print("    Recognizing...")
            query = recognize.recognize_google(audio, language = "en-US")
            print(f"        YOU SAID: {query.lower()}")
        except Exception as exception:
            print(exception)
            print("I didn't quite catch that...")
    return query.lower()

def take_command(): # USED DURING TESTING TO INPUT COMMANDS VIA TEXT
    try:
        query = input(f"{Style.CYAN}YOU:{Style.RESET} ")
    except Exception as exception:
        print(exception)
    return query.lower()

#---------------------------------------------#
#****************** REPLIKA ******************#
#---------------------------------------------#
def Login_Replika():
    usrnme = Replika.find_element(By.ID, "emailOrPhone")
    usrnme.send_keys(config.REPLIKA_EMAIL_LOGIN)  # replika email
    usrnme.send_keys(Keys.RETURN)

    time.sleep(2)

    paswrd = Replika.find_element(By.ID, "login-password")
    paswrd.send_keys(config.REPLIKA_PASSWORD)  # replika password
    paswrd.send_keys(Keys.RETURN)

    WebDriverWait(Replika, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div[1]')))
    pop_up_button = Replika.find_element(By.XPATH, '/html/body/div/div/div[1]/div[1]/button')
    pop_up_button.click()
    print("    REPLIKA logged in!")
    print("------------------------------------------------------------------")

def Recieve_Message_From_Replika():
    old = Replika.find_elements(By.CLASS_NAME, "MessageGroup__MessageGroupRoot-h4dfhv-0.xoUuE")
    time.sleep(10)
    new = Replika.find_elements(By.CLASS_NAME, "MessageGroup__MessageGroupRoot-h4dfhv-0.xoUuE")

    if len(old) != len(new):  # compare old, new
        resWebList = new
        words = ['PM', 'AM', 'thumb up', 'thumb down', 'show more actions', '😊', '💛', ':)']
        msgs = []
        resA = []

        for x in range(len(old)):  # extrapolate differance
            resWebList.remove(old[x])

        for y in range(len(resWebList)):  # convert to string list
            message = resWebList[y].text.split("\n")
            msgs.append(message)
            resA.append(message)

        msg = msgs[0]
        res = resA[0]
        y = 0
        while y < len(msg):  # check though all words     #remove unwanted data
            x = 0
            while x < len(words):  # compare against words
                try:
                    if words[x] in res[y]:
                        res.remove(msg[y])
                    else:
                        pass
                except IndexError:
                    pass
                finally:
                    x += 1
            y += 1
        return res  # return response
    else:
        return False

def Send_Message_To_Replika(msg):
    rep = Replika.find_element(By.ID, "send-message-textarea")
    rep.send_keys(msg)
    rep.send_keys(Keys.RETURN)

def Chat_with_Replika():
    Login_Replika()
    while True:
        message = listen()
        if "goodnight" in message.lower():
            Replika.quit()
            print("------------------------------------------------------------------")
            print(" Kenzie is sleeping...")
            print("    Returning to general commands")
            print("------------------------------------------------------------------")
            break
        else:
            Send_Message_To_Replika(message)  # send to replika
            res = Recieve_Message_From_Replika()
            print(f"{('').join(res)} ")
            speak(f"{('').join(res)}")

#---------------------------------------------#
#****************** COMMAND ******************#
#---------------------------------------------#
def get_time_date():
    if "what is the time" in query:
        return date_time.get_time()
    elif "what is the date" in query:
        return date_time.get_date()

def search_wiki():
    if "what is time" in query:
        time.sleep(2)
        return "Time is the continued sequence of existence and events that occurs in an apparently irreversible succession from the past, through the present, into the future. It is a component quantity of various measurements used to sequence events, to compare the duration of events or the intervals between them, and to quantify rates of change of quantities in material reality or in the conscious experience."
    elif "what is a dog" in query:
        time.sleep(2)
        return "The dog or domestic dog (Canis familiaris or Canis lupus familiaris) is a domesticated descendant of the wolf, and is characterized by an upturning tail. The dog is derived from an ancient, extinct wolf, and the modern wolf is the dog's nearest living relative."
    elif "what is a cat" in query:
        time.sleep(2)
        return "The cat (Felis catus) is a domestic species of small carnivorous mammal.[1][2] It is the only domesticated species in the family Felidae and is often referred to as the domestic cat to distinguish it from the wild members of the family.[4] A cat can either be a house cat, a farm cat or a feral cat; the latter ranges freely and avoids human contact."
    elif "what is a fish" in query:
        time.sleep(2)
        return "Fish are aquatic, craniate, gill-bearing animals that lack limbs with digits. Included in this definition are the living hagfish, lampreys, and cartilaginous and bony fish as well as various extinct related groups. Around 99% of living fish species are ray-finned fish, belonging to the class Actinopterygii, with over 95% belonging to the teleost subgrouping."
    elif "what is time" not in query and "what is a fish" not in query and "what is a cat" not in query and "what is a dog" not in query and "what is the" not in query and "what is the meaning of" not in query and "what is the synonym of" not in query and "what is the antonym of" not in query:
        return wiki.search_wikipedia(query)

def get_google_calendar(query, service):
    def get_events_from_calendar(query, service):
        CALENDAR_STRS = ["what do i have", "do i have plans"]
        for phrase in CALENDAR_STRS:
            if phrase in query.lower():
                date = google_calendar.get_date(query)
                if date:
                    google_calendar.get_events(date, service)
                else:
                    speak("Please Try Again")

    get_events_from_calendar(query, service)
    if "add" in query and "to calendar" in query:
        google_calendar.create_event(query, service)
    elif "delete" in query and "from calendar" in query:
        google_calendar.delete_event(query, service)

def converter():
    converter = currency_convert.RealTimeCurrencyConverter(url='https://api.exchangerate-api.com/v4/latest/USD')
    FROM = str(query.split(' to')[0].replace('convert ', '')).upper()
    TO = str(query.split('to')[1].replace(' ', '')).upper()
    if TO == "USD":
        return f"1 {FROM} is equal to ${converter.convert(FROM, TO, 1)} {TO}"
    else:
        return f"1 {FROM} is equal to {converter.convert(FROM, TO, 1)} {TO}"

def get_news():
    if "the latest news" in query:
        print(news.get_latest_news())
        speak(news.get_latest_news().replace(f"{Style.YELLOW}","").replace(f"{Style.RESET}",""))
    elif "the latest space news" in query:
        print(news.get_space_news())
        speak(news.get_space_news())
    elif "the latest tech news" in query:
        print(news.get_latest_tech_news())
        speak(news.get_latest_tech_news())
    elif "the latest science news" in query:
        print(news.get_latest_science_news())
        speak(news.get_latest_science_news())

def get_movies():
    if "what movies are showing" in query or "get movies":
        print(movies.get_movies_in_theatres())
        speak(movies.get_movies_in_theatres().replace(f"{Style.YELLOW}", "").replace(f"{Style.RESET}", ""))
    elif "what movies are trending" in query or "get trending movies" in query:
        print(movies.get_trending_movies())
        speak(movies.get_trending_movies().replace(f"{Style.YELLOW}", "").replace(f"{Style.RESET}", ""))
    elif "what movies are popular" in query or "get popular movies" in query:
        print(movies.get_popular_movies())
        speak(movies.get_popular_movies().replace(f"{Style.YELLOW}", "").replace(f"{Style.RESET}", ""))

def contacts():
    if "add contact" in query:
        contact_list.add_contact()
    elif "get contact" in query and "list" not in query:
        contact_list.get_contact()
    elif "get contact list" in query:
        contact_list.get_contacts()
    elif "update contact" in query:
        contact_list.update_contact()
    elif "delete contact" in query:
        contact_list.delete_contact()

def shopping():
    if "add to shopping list" in query:
        shopping_list.add_item_to_list()
    elif "update shopping list" in query:
        shopping_list.update_item_in_list()
    elif "delete from shopping list" in query:
        shopping_list.delete_item_from_list()
    elif "get shopping list":
        shopping_list.get_shopping_list()

def todo():
    if "add to todo" in query:
        todo_list.add_task_to_list()
    elif "delete from todo" in query:
        todo_list.delete_task_from_list()
    elif "update todo" in query:
        todo_list.update_task_in_list()
    elif "get todo" in query:
        todo_list.get_todo_list()

def diary_entries():
    while True:
        speak("What would you like to do?")
        query = listen()
        if "add entry" in query:
            diary.add_diary_entry()
            continue
        elif "delete entry" in query:
            diary.delete_diary_entry()
            continue
        elif "update entry" in query:
            diary.update_diary_entry()
            continue
        elif "get entries" in query and "entry" not in query:
            diary.get_diary()
            continue
        elif "get entry" in query:
            diary.get_entry()
            continue
        elif "close diary" in query or "close journal" in query:
            break

def shutdown():
    try:
        Replika.quit()
    except NameError:
        pass
    print("   Shutting down....")
    speak("Shutting down")
    time.sleep(2)
    exit()

###########################################################
#----------------------- MAIN LOOP -----------------------#
###########################################################
if __name__ == "__main__":
    print("\n------------------------------------------------------------------")
    print(" PERSONAL ASSISTANT                                                 ")
    print("------------------------------------------------------------------  ")
    print("Running...\n")
    time.sleep(5)
    WAKE = "hey computer"
    service = google_calendar.authenticate_google_calendar()
    while True:
        print("Listening...")
        query = listen()
        if query.count(WAKE) > 0:
            speak("I am ready")
            query = listen()
            try:
                ### REPLIKA ###
                if "chat" in query:
                    Replika = webdriver.Chrome(PATH)
                    Replika.get("https://my.replika.com/login")
                    Replika.minimize_window()
                    try:
                        Chat_with_Replika()
                        continue
                    except:
                        print(f"{Style.MAGENTA}BOT:{Style.RESET} I am not in the mood to chat at this time.")
                        speak("I am not in the mood to chat at this time.")
                        continue
                ### USELESS FACTS ###
                elif "tell me a fact" in query or "useless fact" in query:
                    fact = facts.get_random_fact()
                    print(f"{Style.MAGENTA}BOT:{Style.RESET} {fact}")
                    speak(fact)
                    continue
                ### HOROSCOPE ###
                elif "horoscope" in query:
                    horoscope = horoscope.get_horoscope(query)
                    print(f"{Style.MAGENTA}BOT:{Style.RESET} {horoscope}")
                    speak(horoscope)
                    continue
                ### MAGIC 8 BALL ###
                elif "magic 8 ball" in query:
                    ball = magic_8_ball.Magic_8_Ball(query)
                    print(f"{Style.MAGENTA}BOT:{Style.RESET} {ball}")
                    speak(ball)
                    continue
                ### TIME & DATE ###
                elif "what is the time" in query or "what is the date" in query:
                    print(f"{Style.MAGENTA}BOT:{Style.RESET} {get_time_date()}")
                    speak(get_time_date())
                    continue
                ### ALARM ###
                elif "set alarm for" in query:
                    alarm.alarm(query)
                    continue
                ### MATH ###
                elif "calculate" in query:
                    print(f"{Style.MAGENTA}BOT:{Style.RESET} {wolfram.calculate(query)}")
                    speak(wolfram.calculate(query))
                    continue
                ### NEWS ###
                elif "what is the latest" in query or "tell me the latest" in query or "get me the latest" in query and "news" in query:
                    get_news()
                    continue
                ### WEATHER ###
                elif "what is the weather" in query or "weather report" in query:
                    weather.weather()
                    continue
                ### MOVIES ###
                elif "movies" in query:
                    get_movies()
                    continue
                ### CONTACTS LIST ###
                elif "contact" in query or "contacts" in query:
                    contacts()
                    continue
                ### SHOPPING LIST ###
                elif "shopping list" in query:
                    shopping()
                    continue
                ### TO DO LIST ###
                elif "todo" in query:
                    todo()
                    continue
                ### DIARY / JOURNAL ###
                elif "open diary" in query or "open journal" in query:
                    diary_entries()
                    continue
                ### WIKIPEDIA ###
                elif "what is" in query or "what are" in query or "who is" in query or "who was" in query:
                    if "the latest" not in query and "news" not in query and "the weather" not in query and "my horoscope" not in query and "useless fact" not in query:
                        print(f"{Style.MAGENTA}BOT:{Style.RESET} Analyzing...")
                        speak("Analyzing...")
                        print(f"{Style.MAGENTA}BOT:{Style.RESET} {search_wiki()}")
                        speak(f"{search_wiki()}")
                        continue
                ### GOOGLE CALENDAR ###
                elif "calendar" in query or "what do i have" in query or "do i have plans" in query:
                    get_google_calendar(query, service)
                    continue
                ### CURRENCY CONVERTER ###
                elif "convert" in query:
                    print(f"{Style.MAGENTA}BOT:{Style.RESET} {converter()}")
                    speak(f"{converter()}")
                    continue
                ### RANDOM JOKE ###
                elif "tell me a joke" in query:
                    joke = jokes.get_random_joke()
                    print(f"{Style.MAGENTA}BOT:{Style.RESET} {joke}")
                    speak(joke)
                    continue
                ### RANDOM ADVICE ###
                elif "give me some advice" in query or "i need some advice" in query:
                    advice = advice.get_random_advice()
                    print(f"{Style.MAGENTA}BOT:{Style.RESET} {advice}")
                    speak(advice)
                    continue
            ### SHUTDOWN PROGRAM ###
            except KeyboardInterrupt:
                shutdown()
            finally:
                if query == "exit" or query == "shutdown" or query == "close":
                    shutdown()
