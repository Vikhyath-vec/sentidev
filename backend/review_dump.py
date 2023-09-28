import pandas as pd
import os
from dotenv import load_dotenv
import aiosql
import psycopg2

queries = aiosql.from_path("sql", "psycopg2")

load_dotenv()

DATABASE = os.getenv("DATABASE")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

conn = psycopg2.connect(
    database=DATABASE,
    user=POSTGRES_USER,
    password=POSTGRES_PASS,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
)
print("Opened database successfully")

df = pd.read_csv("reviews.csv", delimiter='~')

num_rows = df.shape[0]
print(num_rows)
for i in range(num_rows):
    review = df['Review'][i]
    rating = df['Rating'][i]
    movie = df['Movie Name'][i]
    date = df['Date'][i]
    title = df['Title'][i]
    
    # Convert the date to SQL date format. The date is of the form DD monthNane YYYY
    date = date.split()
    day = date[0]
    month = date[1]
    year = date[2]
    if len(day) == 1:
        day = '0' + day
    if month == 'January':
        month = '01'
    elif month == 'February':
        month = '02'
    elif month == 'March':
        month = '03'
    elif month == 'April':
        month = '04'
    elif month == 'May':
        month = '05'
    elif month == 'June':
        month = '06'
    elif month == 'July':
        month = '07'
    elif month == 'August':
        month = '08'
    elif month == 'September':
        month = '09'
    elif month == 'October':
        month = '10'
    elif month == 'November':
        month = '11'
    elif month == 'December':
        month = '12'

    date = year + '-' + month + '-' + day
    motion_picture_id = queries.get_motion_picture_id(conn, title=movie, mtype=1)
    queries.insert_review(conn, motion_picture_id=motion_picture_id, title=title, rating=int(rating), review=review, review_date=date)
    conn.commit()
