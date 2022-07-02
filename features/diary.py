import datetime, pandas, time, main

from db import db
from config import Style

def add_diary_entry():
    while True:
        current_date_time = datetime.datetime.now()
        conn = db.create_connection()
        cursor = conn.cursor()
        main.speak("What is the title of the entry?")
        TITLE = main.listen().title()
        main.speak("WHat is the content of the entry?")
        CONTENT = main.listen().title()
        cursor.execute(f"INSERT INTO diary (Date, Title, Content) VALUES ('{str(current_date_time).strip()[:16]}', '{TITLE}', '{CONTENT}');")
        conn.commit()
        print(f"Entry added.")
        main.speak("Entry added.")
        main.speak("Would you like to add another entry?")
        run_again = main.listen().lower()
        while run_again not in ("yes", "no"):
            main.speak("Please say yes or no.")
            main.speak("Would you like to add another entry?")
            run_again = main.listen().lower()
        if run_again == "yes":
            add_diary_entry()
        elif run_again == "no":
            break

def update_diary_entry():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        print(pandas.read_sql_query("SELECT * from diary", conn))
        diary = cursor.execute("SELECT * from diary;")
        for entry in diary:
            main.speak(f"Entry I.D. {entry[0]} Title: {entry[2]}")
        main.speak("What is the I.D. of the entry you would like to update?")
        update_item = main.listen()
        cursor.execute(f"SELECT * FROM diary WHERE EntryID = {update_item};")
        result = cursor.fetchall()
        main.speak("Would you like to update the Title or the Content?")
        x = main.listen().upper()
        while x not in ('TITLE', 'CONTENT'):
            main.speak("Please say Title or Content.")
            main.speak("Would you like to update the Title or the Content?")
            print("Please select 'TITLE' or 'CONTENT'")
            x = main.listen().upper()
        if x == "TITLE":
            main.speak("What is the new title?")
            TITLE = main.listen().title()
            CONTENT = result[3]
        elif x == "CONTENT":
            TITLE = result[2]
            main.speak("What is the new content?")
            CONTENT = main.listen().capitalize()
        cursor.execute(f"UPDATE diary SET Title = '{TITLE}', Content = '{CONTENT}' WHERE EntryID = {update_item};")
        conn.commit()
        print(f"Entry updated.")
        main.speak("What is the content?")
        break

def delete_diary_entry():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        print(pandas.read_sql_query("SELECT * from diary", conn))
        diary = cursor.execute("SELECT * FROM diary;")
        for entry in diary:
            main.speak(f"Entry ID: {entry[0]} Title: {entry[2]}")
        main.speak("What is the I.D. of the entry you would like to delete?")
        update_item = main.listen()
        cursor.execute(f"DELETE FROM diary WHERE EntryID = {update_item};")
        conn.commit()
        print("Entry deleted")
        main.speak("Entry deleted.")
        break

def get_diary():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        sql_query = cursor.execute("SELECT * from diary;")
        results = sql_query.fetchall()
        if len(results) == 0:
            print("No entries found")
            main.speak("No entries found.")
            break
        else:
            main.speak("The title of your entries are...")
            for item in results:
                print(f"{Style.CYAN}DATE:{Style.RESET} {item[1]} {Style.YELLOW}TITLE:{Style.RESET} {item[2]}")
                main.speak(f"{item[2]}")
            print("\n")
            break

def get_entry():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        sql_query = cursor.execute("SELECT * from diary;")
        results = sql_query.fetchall()
        if len(results) == 0:
            print("No entries found")
            main.speak("No entries found.")
            break
        else:
            main.speak("The I.D. and titles of your entries are...")
            for item in results:
                print(f"{Style.CYAN}ID:{Style.RESET} {item[0]} {Style.YELLOW}TITLE:{Style.RESET} {item[2]}")
                main.speak(f"{item[2]}")
            main.speak("What is the I.D. of the entry?")
            entry_id = main.listen()
            cursor.execute(f"SELECT * FROM diary WHERE EntryID = {entry_id};")
            entry = cursor.fetchall()
            for content in entry:
                print(f"TITLE: {Style.CYAN}{content[2]}{Style.RESET}   CREATED ON: {Style.YELLOW}{content[1]}{Style.RESET}")
                print(f"{content[3]}\n")
                main.speak(f"{content[2]}")
                time.sleep(2)
                main.speak(f"{content[3]}")
            break