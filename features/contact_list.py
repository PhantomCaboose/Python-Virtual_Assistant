import main
from db import db
from config import Style

def add_contact():
    conn = db.create_connection()
    cursor = conn.cursor()
    while True:
        main.speak("What is the first name of the contact?")
        FIRST_NAME = main.listen().capitalize()
        main.speak("What is the last name of the contact?")
        LAST_NAME = main.listen().capitalize()
        main.speak("What is the contact's phone number?")
        PHONE_NUMBER = main.listen()
        if " " in PHONE_NUMBER:
            PHONE_NUMBER = PHONE_NUMBER.replace(" ", "")
        elif "-" in PHONE_NUMBER:
            PHONE_NUMBER = PHONE_NUMBER.replace("-","")
        if len(PHONE_NUMBER) != 10:
            print("INVALID PHONE NUMBER")
            main.speak("Invalid phone number")
            break
        main.speak("What is the birth month of the contact?")
        BIRTHDAY_MONTH = main.listen()
        if BIRTHDAY_MONTH == "01" or BIRTHDAY_MONTH == "1":
            BIRTHDAY_MONTH = "January"
        elif BIRTHDAY_MONTH == "02" or BIRTHDAY_MONTH == "2":
            BIRTHDAY_MONTH = "February"
        elif BIRTHDAY_MONTH == "03" or BIRTHDAY_MONTH == "3":
            BIRTHDAY_MONTH = "March"
        elif BIRTHDAY_MONTH == "04" or BIRTHDAY_MONTH == "4":
            BIRTHDAY_MONTH = "April"
        elif BIRTHDAY_MONTH == "05" or BIRTHDAY_MONTH == "5":
            BIRTHDAY_MONTH = "May"
        elif BIRTHDAY_MONTH == "06" or BIRTHDAY_MONTH == "6":
            BIRTHDAY_MONTH = "June"
        elif BIRTHDAY_MONTH == "07" or BIRTHDAY_MONTH == "7":
            BIRTHDAY_MONTH = "July"
        elif BIRTHDAY_MONTH == "08" or BIRTHDAY_MONTH == "8":
            BIRTHDAY_MONTH = "August"
        elif BIRTHDAY_MONTH == "09" or BIRTHDAY_MONTH == "9":
            BIRTHDAY_MONTH = "September"
        elif BIRTHDAY_MONTH == "10":
            BIRTHDAY_MONTH = "October"
        elif BIRTHDAY_MONTH == "11":
            BIRTHDAY_MONTH = "November"
        elif BIRTHDAY_MONTH == "12":
            BIRTHDAY_MONTH = "December"
        elif BIRTHDAY_MONTH > "12" or BIRTHDAY_MONTH < "01":
            print("NOT A VALID MONTH")
            main.speak(f"That is not a valid month")
            break
        else:
            if BIRTHDAY_MONTH is not None:
                BIRTHDAY_MONTH = BIRTHDAY_MONTH.capitalize()
            elif BIRTHDAY_MONTH == "none":
                BIRTHDAY_MONTH = ""
            else:
                if BIRTHDAY_MONTH != "January" or BIRTHDAY_MONTH != "February":
                    if BIRTHDAY_MONTH != "March" or BIRTHDAY_MONTH != "April":
                        if BIRTHDAY_MONTH != "May" or BIRTHDAY_MONTH != "June":
                            if BIRTHDAY_MONTH != "July" or BIRTHDAY_MONTH != "August":
                                if BIRTHDAY_MONTH != "September" or BIRTHDAY_MONTH != "October":
                                    if BIRTHDAY_MONTH != "November" or BIRTHDAY_MONTH != "December":
                                        print("NOT A VALID MONTH")
                                        main.speak("That is not a valid month.")
                                        break

        main.speak("What is the day of their birthday?")
        BIRTHDAY_DAY = main.listen()
        if BIRTHDAY_MONTH == "January" or BIRTHDAY_MONTH == "March" or BIRTHDAY_MONTH == "May" or BIRTHDAY_MONTH == "July" or BIRTHDAY_MONTH == "August" or BIRTHDAY_MONTH == "October" or BIRTHDAY_MONTH == "December":
            if "0" < BIRTHDAY_DAY > "31":
                print(f"INVALID DAY FOR {BIRTHDAY_MONTH}. {BIRTHDAY_MONTH} has 31 Days")
                main.speak(f"That is not a valid day for {BIRTHDAY_MONTH}. {BIRTHDAY_MONTH} has 31 days.")
                break
            else:
                BIRTHDAY_DAY = BIRTHDAY_DAY
        elif BIRTHDAY_MONTH == "April" or BIRTHDAY_MONTH == "June" or BIRTHDAY_MONTH == "September" or BIRTHDAY_MONTH == "November":
            if "0" < BIRTHDAY_DAY > "30":
                print(f"INVALID DAY FOR {BIRTHDAY_MONTH}. {BIRTHDAY_MONTH} has 30 Days")
                main.speak(f"That is not a valid day for {BIRTHDAY_MONTH}. {BIRTHDAY_MONTH} has 30 days.")
                break
            else:
                BIRTHDAY_DAY = BIRTHDAY_DAY
        elif BIRTHDAY_MONTH == "February":
            if "0" < BIRTHDAY_DAY > "29":
                print(f"INVALID DAY FOR {BIRTHDAY_MONTH}. {BIRTHDAY_MONTH} has 28 Days (29 on Leap Years)")
                main.speak(f"That is not a valid day for {BIRTHDAY_MONTH}. {BIRTHDAY_MONTH} has 28 days. (29 on Leap Years).")
                break
            else:
                if BIRTHDAY_DAY is not None:
                    BIRTHDAY_DAY = BIRTHDAY_DAY
                elif BIRTHDAY_DAY == "none":
                    BIRTHDAY_DAY = ""
                else:
                    BIRTHDAY_DAY = ""

        PHONE = f"({PHONE_NUMBER[:3]})-{PHONE_NUMBER[3:6]}-{PHONE_NUMBER[6:10]}"
        BIRTHDAY = f"{BIRTHDAY_MONTH}-{BIRTHDAY_DAY}"

        cursor.execute(f"INSERT INTO contacts (Last_Name, First_Name, PhoneNumber, Birthday) VALUES ('{LAST_NAME}', '{FIRST_NAME}', '{PHONE}', '{BIRTHDAY}');")
        conn.commit()
        print("Contact Created")
        main.speak("Contact successfully added")
        break

def get_contact():
    conn = db.create_connection()
    cursor = conn.cursor()
    while True:
        try:
            main.speak("What is the name of the contact?")
            NAME = main.listen()
            FIRST_NAME = NAME.split(' ')[0].capitalize()
            LAST_NAME = NAME.split(' ')[1].capitalize()
            sql_query = cursor.execute(f"Select * FROM contacts WHERE Last_Name = '{LAST_NAME}' AND First_Name = '{FIRST_NAME}';")
            contacts = sql_query.fetchall()
            if len(contacts) == 0:
                print("No records found\n")
                main.speak("No contacts found by that name.")
                break
            else:
                for item in contacts:
                    print(f"\n{Style.YELLOW}Name:{Style.RESET} {item[2]} {item[1]}   {Style.YELLOW}Birthday:{Style.RESET} {item[4]}")
                    print(f"{Style.YELLOW}Phone Number:{Style.RESET} {item[3]}\n")
                    main.speak(f"Contact: {item[2]} {item[1]}... Birthday is {item[4]} Phone number {item[3]}")
                break
        except IndexError:
            print("Please provide first and last name of contact")
            main.speak("Please provide first and last name of the contact")
            break

def get_contacts():
    conn = db.create_connection()
    cursor = conn.cursor()
    while True:
        try:
            sql_query = cursor.execute(f"Select * FROM contacts;")
            contacts = sql_query.fetchall()
            if len(contacts) == 0:
                print("No records found\n")
                main.speak("No contacts found")
                break
            else:
                for item in contacts:
                    print(f"\n{Style.YELLOW}Name:{Style.RESET} {item[2]} {item[1]}   {Style.YELLOW}Birthday:{Style.RESET} {item[4]}")
                    print(f"{Style.YELLOW}Phone Number:{Style.RESET} {item[3]}\n")
                    main.speak(f"Contact: {item[2]} {item[1]}... Birthday is {item[4]} Phone number {item[3]}")
                break
        except IndexError:
            break

def update_contact():
    conn = db.create_connection()
    cursor = conn.cursor()
    while True:
        try:
            main.speak("What is the name of the contact?")
            NAME = main.listen()
            FIRST_NAME = NAME.split(' ')[0].capitalize()
            LAST_NAME = NAME.split(' ')[1].capitalize()
            main.speak("Would you like to update the contact's first name, last name, birthday, or phone number?")
            update_query = main.listen().lower()
            if "last name" in update_query:
                NEW_LAST_NAME = main.listen().capitalize()
                cursor.execute(f"UPDATE contacts SET Last_Name = '{NEW_LAST_NAME}' WHERE Last_Name = '{LAST_NAME}' AND First_Name = '{FIRST_NAME}';")
                conn.commit()
                print("Updated Successfully")
                main.speak("Contact updated.")
                break
            elif "first name" in update_query:
                NEW_FIRST_NAME = main.listen().capitalize()
                cursor.execute(f"UPDATE contacts SET First_Name = '{NEW_FIRST_NAME}' WHERE Last_Name = '{LAST_NAME}' AND First_Name = '{FIRST_NAME}';")
                conn.commit()
                print("Updated Successfully")
                main.speak("Contact updated.")
                break
            elif "phone number" in update_query:
                NEW_PHONE = main.listen()
                if " " in NEW_PHONE:
                    NEW_PHONE = NEW_PHONE.replace(" ", "")
                elif "-" in NEW_PHONE:
                    NEW_PHONE = NEW_PHONE.replace("-","")
                if len(NEW_PHONE) != 10:
                    print("INVALID PHONE NUMBER")
                    main.speak("That is an invalid phone number.")
                    break
                PHONE = f"({NEW_PHONE[:3]})-{NEW_PHONE[3:6]}-{NEW_PHONE[6:10]}"
                cursor.execute(f"UPDATE contacts SET PhoneNumber = '{PHONE}' WHERE Last_Name = '{LAST_NAME}' AND First_Name = '{FIRST_NAME}';")
                conn.commit()
                print("Updated Successfully")
                main.speak("Contact updated.")
                break
            elif "birthday" in update_query:
                NEW_BIRTH_MONTH = main.listen()
                if NEW_BIRTH_MONTH == "01" or NEW_BIRTH_MONTH == "1":
                    NEW_BIRTH_MONTH = "January"
                elif NEW_BIRTH_MONTH == "02" or NEW_BIRTH_MONTH == "2":
                    NEW_BIRTH_MONTH = "February"
                elif NEW_BIRTH_MONTH == "03" or NEW_BIRTH_MONTH == "3":
                    NEW_BIRTH_MONTH = "March"
                elif NEW_BIRTH_MONTH == "04" or NEW_BIRTH_MONTH == "4":
                    NEW_BIRTH_MONTH = "April"
                elif NEW_BIRTH_MONTH == "05" or NEW_BIRTH_MONTH == "5":
                    NEW_BIRTH_MONTH = "May"
                elif NEW_BIRTH_MONTH == "06" or NEW_BIRTH_MONTH == "6":
                    NEW_BIRTH_MONTH = "June"
                elif NEW_BIRTH_MONTH == "07" or NEW_BIRTH_MONTH == "7":
                    NEW_BIRTH_MONTH = "July"
                elif NEW_BIRTH_MONTH == "08" or NEW_BIRTH_MONTH == "8":
                    NEW_BIRTH_MONTH = "August"
                elif NEW_BIRTH_MONTH == "09" or NEW_BIRTH_MONTH == "9":
                    NEW_BIRTH_MONTH = "September"
                elif NEW_BIRTH_MONTH == "10":
                    NEW_BIRTH_MONTH = "October"
                elif NEW_BIRTH_MONTH == "11":
                    NEW_BIRTH_MONTH = "November"
                elif NEW_BIRTH_MONTH == "12":
                    NEW_BIRTH_MONTH = "December"
                elif NEW_BIRTH_MONTH > "12" or NEW_BIRTH_MONTH < "01":
                    print("NOT A VALID MONTH")
                    main.speak("That is not a valid month.")
                    break
                else:
                    if NEW_BIRTH_MONTH is not None:
                        NEW_BIRTH_MONTH = NEW_BIRTH_MONTH.capitalize()
                    else:
                        if NEW_BIRTH_MONTH != "January" or NEW_BIRTH_MONTH != "February":
                            if NEW_BIRTH_MONTH != "March" or NEW_BIRTH_MONTH != "April":
                                if NEW_BIRTH_MONTH != "May" or NEW_BIRTH_MONTH != "June":
                                    if NEW_BIRTH_MONTH != "July" or NEW_BIRTH_MONTH != "August":
                                        if NEW_BIRTH_MONTH != "September" or NEW_BIRTH_MONTH != "October":
                                            if NEW_BIRTH_MONTH != "November" or NEW_BIRTH_MONTH != "December":
                                                print("NOT A VALID MONTH")
                                                main.speak("That is not a valid month")
                                                break

                NEW_BIRTH_DAY = main.listen()
                if NEW_BIRTH_MONTH == "January" or NEW_BIRTH_MONTH == "March" or NEW_BIRTH_MONTH == "May" or NEW_BIRTH_MONTH == "July" or NEW_BIRTH_MONTH == "August" or NEW_BIRTH_MONTH == "October" or NEW_BIRTH_MONTH == "December":
                    if "0" < NEW_BIRTH_DAY > "31":
                        print(f"INVALID DAY FOR {NEW_BIRTH_MONTH}. {NEW_BIRTH_MONTH} has 31 Days")
                        main.speak(f"That is an invalid day for {NEW_BIRTH_MONTH}. {NEW_BIRTH_MONTH} has 31 Days")
                        break
                    else:
                        NEW_BIRTH_DAY = NEW_BIRTH_DAY
                elif NEW_BIRTH_MONTH == "April" or NEW_BIRTH_MONTH == "June" or NEW_BIRTH_MONTH == "September" or NEW_BIRTH_MONTH == "November":
                    if "0" < NEW_BIRTH_DAY > "30":
                        print(f"INVALID DAY FOR {NEW_BIRTH_MONTH}. {NEW_BIRTH_MONTH} has 30 Days")
                        main.speak(f"That is an invalid day for {NEW_BIRTH_MONTH}. {NEW_BIRTH_MONTH} has 30 Days")
                        break
                    else:
                        NEW_BIRTH_DAY = NEW_BIRTH_DAY
                elif NEW_BIRTH_MONTH == "February":
                    if "0" < NEW_BIRTH_DAY > "29":
                        print(f"INVALID DAY FOR {NEW_BIRTH_MONTH}. {NEW_BIRTH_MONTH} has 28 Days (29 on Leap Years)")
                        main.speak(f"That is an invalid day for {NEW_BIRTH_MONTH}. {NEW_BIRTH_MONTH} has 28 Days. (29 on Leap Years).")
                        break
                    else:
                        if NEW_BIRTH_DAY is not None:
                            NEW_BIRTH_DAY = NEW_BIRTH_DAY
                        else:
                            NEW_BIRTH_DAY = ""

                NEW_BIRTHDAY = f"{NEW_BIRTH_MONTH}-{NEW_BIRTH_DAY}"
                cursor.execute(f"UPDATE contacts SET Birthday = '{NEW_BIRTHDAY}' WHERE Last_Name = '{LAST_NAME}' AND First_Name = '{FIRST_NAME}';")
                conn.commit()
                print("Updated Successfully")
                main.speak("Contact updated.")
                break
        except IndexError:
            print("Please provide first and last name of contact")
            main.speak("Please provide the first and last name of the contact")
            break

def delete_contact():
    conn = db.create_connection()
    cursor = conn.cursor()
    while True:
        try:
            main.speak("What is the name of the contact?")
            NAME = main.listen()
            FIRST_NAME = NAME.split(' ')[0].capitalize()
            LAST_NAME = NAME.split(' ')[1].capitalize()
            cursor.execute(f"DELETE FROM contacts WHERE Last_Name = '{LAST_NAME}' AND First_Name = '{FIRST_NAME}';")
            conn.commit()
            print("Contact Deleted")
            main.speak("Contact deleted.")
            break
        except IndexError:
            print("Please provide first and last name of contact")
            main.speak("Please provide the first and last name of the contact.")
            break
