import sqlite3
from datetime import datetime

conn = sqlite3.connect("news.db")      
cursor = conn.cursor()

username = input("Enter your username : ")

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS USERS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERNAME TEXT,
    CATEGORY TEXT,
    AUTHOR TEXT,
    TITLE TEXT,
    PUBLISHED_AT TEXT,
    WATCH_TIME TEXT
    )
    """)


def search_by_category():
    print(f'\n{username} we have lastest news across 4 categories ')
    categories = ["A : business","B : health","C : entertainment","D : technology"]
    for i in categories:
        print(i)

    while True : 
        user_cat = input("Which one you want : ").upper()
        match user_cat:
            case "A":
                user_cat="business"
                break

            case "B":
                user_cat="health"
                break

            case "C":
                user_cat="entertainment"
                break

            case "D":
                user_cat="technology"
                break

            case _ :
                print("Invalid input..!!")


    cursor.execute("""
    SELECT SOURCE,AUTHOR,TITLE,CONTENT,PUBLISHED_AT FROM fetchdata WHERE CATEGORY=? AND CONTENT IS NOT NULL limit 3
    """,(user_cat,))

    cuurent_time = datetime.now().isoformat()

    RESULT = cursor.fetchall()
    for x in RESULT:
        cursor.execute(""" 
        INSERT INTO USERS (USERNAME,CATEGORY,AUTHOR,TITLE,PUBLISHED_AT,WATCH_TIME) VALUES(?,?,?,?,?,?)
        """,(username,user_cat,x[1],x[2],x[4],cuurent_time))

        print(f"\n PUBLISHED AT : {x[4]} \n Source : {x[0]} \n Author : {x[1]} \n TITLE : {x[2]} \n CONTENT : {x[3]} ")


    conn.commit()


# -----------------------------------------------------------------
def dynamic_search(keyword=None, source=None,category=None, start_date=None, end_date=None):
    query = "SELECT * FROM fetchdata WHERE 1=1"
    params = []

    if keyword:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.append(f"%{keyword}%")
        params.append(f"%{keyword}%")

    if source:
        query += " AND source = ?"
        params.append(source)
        
    if category:
        query += " AND category = ?"
        params.append(category)

    if start_date and end_date:
        query += " AND published_at BETWEEN ? AND ?"
        params.append(start_date)
        params.append(end_date)

    cursor.execute(query, params)
    result = cursor.fetchall()

    cuurent_time = datetime.now().isoformat()

    for x in result:
     cursor.execute(""" 
     INSERT INTO USERS (USERNAME,CATEGORY,AUTHOR,TITLE,PUBLISHED_AT,WATCH_TIME) VALUES(?,?,?,?,?,?)
        """,(username,x[1],x[3],x[4],x[7],cuurent_time))

     print(f"\n PUBLISHED AT : {x[7]} \n Source : {x[2]} \n Author : {x[3]} \n TITLE : {x[4]} \n CONTENT : {x[6]} ")
    conn.commit()

dynamic_search("covid") 
search_by_category()   

conn.close()