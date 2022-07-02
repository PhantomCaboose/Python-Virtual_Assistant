import datetime, pandas, main

from db import db
from config import Style

def add_task_to_list():
    while True:
        current_date_time = datetime.datetime.now()
        conn = db.create_connection()
        cursor = conn.cursor()
        main.speak("What is the task?")
        NAME = main.listen().capitalize()
        cursor.execute(f"INSERT INTO todo_list (Name, Date) VALUES ('{NAME}', '{str(current_date_time).strip()[:16]}');")
        conn.commit()
        print(f"Task added to list.")
        main.speak("Task added to todo list.")
        main.speak("Would you like to add another task?")
        run_again = main.listen().lower()
        while run_again not in ("yes", "no"):
            main.speak("Please say yes or no.")
            main.speak("Would you like to add another task?")
            run_again = main.listen().lower()
        if run_again == "yes":
            add_task_to_list()
        elif run_again == "no":
            break

def update_task_in_list():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        print(pandas.read_sql_query("SELECT * from task_list", conn))
        todo = cursor.execute("SELECT * from task_list;")
        for task in todo:
            main.speak(f"ID: {task[0]}  Task: {task[1]}")
        main.speak("What is the ID of the task you would like to update?")
        update_item = main.listen()
        cursor.execute(f"SELECT * FROM task_list WHERE ItemID = {update_item};")
        main.speak("What is the new task?")
        TASK = main.listen()
        cursor.execute(f"UPDATE todo_list SET Name = '{TASK}' WHERE ItemID = {update_item};")
        conn.commit()
        print(f"Task updated.")
        print("Task updated in todo list")
        break

def delete_task_from_list():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        print(pandas.read_sql_query("SELECT * from todo_list", conn))
        todo = cursor.execute("SELECT * from todo_list;")
        for task in todo:
            main.speak(f"ID: {task[0]} Task: {task[1]}")
        main.speak("What is the I.D. of the task you want to delete?")
        update_item = main.listen()
        cursor.execute(f"DELETE FROM todo_list WHERE ItemID = {update_item};")
        conn.commit()
        print("Task deleted")
        main.speak("Task deleted from todo list.")
        break

def get_todo_list():
    while True:
        conn = db.create_connection()
        cursor = conn.cursor()
        sql_query = cursor.execute("SELECT * from todo_list;")
        results = sql_query.fetchall()
        if len(results) == 0:
            print("No items in list")
            main.speak("There are no tasks todo")
            break
        else:
            main.speak("You have the following tasks on your todo list")
            for item in results:
                print(f"{Style.YELLOW}TASK:{Style.RESET} {item[1]} {Style.YELLOW}DATE CREATED:{Style.RESET} {item[2]}")
                main.speak(f"{item[1]}")
            break