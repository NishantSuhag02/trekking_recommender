from fastapi import FastAPI
import sqlite3
from recommeder.engine import TrekRecommender
from chatbot.chatbot import ChatBot

app = FastAPI()

db_path = "treks.db"

recommender = TrekRecommender(db_path)
bot = ChatBot(db_path)

def get_db():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    # row_factory = sqlite3.row converts the records or rows into dict 
    # like data so that we can fetch data using column name instead of indices.
    conn.row_factory = sqlite3.Row
    return conn

@app.get('/')
def home():
    return {"message":"Treak Recommender API Running."}

@app.get('/recommend')
def recommend(month: str, difficulty: str, days: int, budget: int):
    results = recommender.recommend(month,difficulty,days,budget)
    return results

@app.get('/chat')
def chat(user_input: str):
    results = bot.chat(user_input)
    return results

@app.get('/treks')
def get_all_treks():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM treks')
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

@app.get('/trek/{name}')
def get_trek(name: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM treks WHERE name = ?',(name,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)
    
    return {'error':'Trek Not Found!'}



