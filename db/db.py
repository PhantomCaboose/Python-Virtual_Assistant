import sqlite3
from sqlite3 import Error

DATABASE_LOCATION = r'C:\Users\vbrad\PycharmProjects\Github Projects\Virtual_Assistant\db\database.db'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_LOCATION)
        cursor = conn.cursor()
        cursor.executescript("""CREATE TABLE IF NOT EXISTS contacts (ContactID INTEGER PRIMARY KEY,
            Last_Name TEXT, First_Name TEXT, PhoneNumber TEXT, Birthday TEXT);
            
            CREATE TABLE IF NOT EXISTS shopping_list (ItemID INTEGER PRIMARY KEY, Item TEXT, Category Text);

            CREATE TABLE IF NOT EXISTS todo_list (ItemID INTEGER PRIMARY KEY, Name TEXT, Date TIMESTAMP);
            
            CREATE TABLE IF NOT EXISTS diary (EntryID INTEGER PRIMARY KEY, Date TIMESTAMP, Title TEXT, Content TEXT);
            """)
        conn.commit()
    except Error as e:
        print(e)
    return conn
