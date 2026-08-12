import requests
import sqlite3

import os
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()
api_key = os.getenv("MY_API_KEY")

url = "https://newsapi.org/v2/top-headlines"
header = {
    "Authorization":api_key
}
categories = ["business","health","entertainment","technology"]

conn = sqlite3.connect("news.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS fetchdata (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
CATEGORY TEXT,
SOURCE TEXT,
AUTHOR TEXT,
TITLE TEXT,
DESCRIPTION TEXT,
CONTENT TEXT,
PUBLISHED_AT TEXT,
FETCHED_AT TEXT
)
""")

while True:

 for i in categories:
    params = {
    "country":"us",
    "category":i
   }
    try :
       response = requests.get(url,params,headers=header)
       print("STATUS CODE:", response.status_code)
       Json_Data = response.json()

       if len(Json_Data["articles"]) ==0:
        raise ValueError(f"{i} Category has zero news today") 

       for x in range(min(len(Json_Data["articles"]),5)):
        current_data = Json_Data["articles"][x]
        # SAFE CHECK: Prevents KeyError if keys are null or missing from the API then fills it with NONW
        SOURCE = current_data["source"]["name"] if current_data.get("source") else "Unknown"
        AUTHOR = current_data.get("author")
        TITLE = current_data.get("title")
        DESCRIPTION = current_data.get("description")
        CONTENT = current_data.get("content")
        PUBLISHED_AT = current_data.get("publishedAt")
        FETCHED_AT = datetime.now().isoformat()


        cursor.execute("""
        select TITLE,DESCRIPTION,CONTENT from fetchdata where TITLE=? AND DESCRIPTION=? AND CONTENT=?
        """,(TITLE,DESCRIPTION,CONTENT))
        re=cursor.fetchall() 
        if len(re) == 0 :
           cursor.execute("""
             INSERT INTO fetchdata(CATEGORY,SOURCE,AUTHOR,TITLE,DESCRIPTION,CONTENT,PUBLISHED_AT,FETCHED_AT) VALUES (?,?,?,?,?,?,?,?)
              """,(i,SOURCE,AUTHOR,TITLE,DESCRIPTION,CONTENT,PUBLISHED_AT,FETCHED_AT))
        else:
           continue  
       conn.commit()
          

    except Exception as e:  
        print(f"Error occured :{e}")

 print("Sleeping for 24 hours...")
 time.sleep(5) # As of now for testing added only 10 sec..