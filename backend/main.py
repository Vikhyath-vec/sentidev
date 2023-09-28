from datetime import datetime
from typing import Dict, List, Union
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pytz import timezone
import psycopg2
import os
from dotenv import load_dotenv
import aiosql
from google.auth import exceptions
from omdb_utils import get_motion_picture_info
from scraping_utils import extract_tagline

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

# queries.create_schema(conn)
# print("Schema created successfully")
# conn.commit()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/add")
async def add_motion_picture(info: Request):
    req_info = await info.json()
    title = req_info["title"]

    if title is None:
        return {"Result": "Failure"}
    motion_picture_info = get_motion_picture_info(title)
    if "Error" in motion_picture_info.keys():
        return {"Result": "Failure"}
    motion_picture_info["tagline"] = extract_tagline(title)
    if motion_picture_info["type"] == 0:
        motion_picture_id = queries.insert_movie(
            conn,
            title=motion_picture_info["title"],
            tagline=motion_picture_info["tagline"],
            description=motion_picture_info["description"],
            poster=motion_picture_info["poster"],
            director=motion_picture_info["director"],
            tmdb_id=motion_picture_info["tmdb_id"]
        )
    elif motion_picture_info["type"] == 1:
        motion_picture_id = queries.insert_show(
            conn,
            title=motion_picture_info["title"],
            tagline=motion_picture_info["tagline"],
            description=motion_picture_info["description"],
            poster=motion_picture_info["poster"],
            tmdb_id=motion_picture_info["tmdb_id"]
        )
    
    for actor in motion_picture_info["actors"].split(", "):
        actor_id = queries.insert_actor(conn, name=actor)
        queries.insert_motion_picture_actor(conn, motion_picture_id=motion_picture_id, actor_id=actor_id)
    
    for writer in motion_picture_info["writers"].split(", "):
        writer_id = queries.insert_writer(conn, name=writer)
        queries.insert_motion_picture_writer(conn, motion_picture_id=motion_picture_id, writer_id=writer_id)
    
    for genre in motion_picture_info["genres"].split(", "):
        genre_id = queries.insert_genre(conn, name=genre)
        queries.insert_motion_picture_genre(conn, motion_picture_id=motion_picture_id, genre_id=genre_id)
    
    conn.commit()
    return {"Result": "Success"}
