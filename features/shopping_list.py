import pandas, main

from db import db
from config import Style

def add_item_to_list():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        main.speak("What is the name of the Item?")
        ITEM = main.listen().capitalize()
        main.speak("What is the category of the item?")
        CATEGORY = main.listen().capitalize()
        cursor.execute(f"INSERT INTO shopping_list (Item, Category) VALUES ('{ITEM}', '{CATEGORY}');")
        conn.commit()
        print(f"Item added to list.")
        main.speak("Item added to shopping list.")
        main.speak("Would you like to add another item?")
        run_again = main.listen().lower()
        while run_again not in ("yes", "no"):
            main.speak("Please say yes or no.")
            main.speak("Would you like to add another item?")
            run_again = main.listen().lower()
        if run_again == "yes":
            add_item_to_list()
        elif run_again == "no":
            break

def update_item_in_list():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        print(pandas.read_sql_query("SELECT * from shopping_list", conn))
        shop = cursor.execute("SELECT * from shopping_list;")
        for item in shop:
            main.speak(f"Item ID: {item[0]} Item: {item[1]}")
        main.speak("What is the I.D. of the item?")
        update_item = main.listen()
        cursor.execute(f"SELECT * FROM shopping_list WHERE ItemID = {update_item};")
        result = cursor.fetchall()
        main.speak("Would you like to update the Item or the Category?")
        x = main.listen().upper()
        while x not in ('ITEM', 'CATEGORY'):
            main.speak("Please state if you would like to update the Item or the Category.")
            print("Please select 'ITEM' or 'CATEGORY'")
            x = main.listen().upper()
        if x == "ITEM":
            main.speak("What is the new name for the item?")
            ITEM = main.listen().capitalize()
            CATEGORY = result[2]
        elif x == "CATEGORY":
            ITEM = result[1]
            main.speak(f"What is the new category for the item {ITEM}")
            CATEGORY = main.listen().capitalize()
        cursor.execute(f"UPDATE shopping_list SET Item = '{ITEM}', Category = '{CATEGORY}' WHERE ItemID = {update_item};")
        conn.commit()
        print(f"Item updated.")
        main.speak("Item updated.")
        break

def delete_item_from_list():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        print(pandas.read_sql_query("SELECT * from shopping_list", conn))
        shop = cursor.execute("SELECT * from shopping_list;")
        for item in shop:
            main.speak(f"Item ID: {item[0]} Item: {item[1]}")
        main.speak("What is the I.D. of the item?")
        update_item = main.listen()
        cursor.execute(f"DELETE FROM shopping_list WHERE ItemID = {update_item};")
        conn.commit()
        print("Item deleted")
        main.speak("Item deleted.")
        break

def get_shopping_list():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        sql_query = cursor.execute("SELECT * from shopping_list;")
        results = sql_query.fetchall()
        if len(results) == 0:
            print("No items in list")
            main.speak("There are no items in the shopping list.")
            break
        else:
            for item in results:
                print(f"{Style.YELLOW}ITEM:{Style.RESET} {item[1]} {Style.YELLOW}CATEGORY:{Style.RESET} {item[2]}")
                main.speak(f"Item: {item[1]} Category: {item[2]}")
            break