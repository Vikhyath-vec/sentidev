import requests
import json
import os
from dotenv import load_dotenv
from tmdb_utils import get_motion_picture_details_by_name

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

def get_motion_picture_info(title: str) -> dict:
    """Get movie information from OMDB API"""
    title = title.replace(" ", "+")
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    response = requests.get(url)
    json_data = json.loads(response.text)
    if json_data["Response"] == "False":
        return {"Error": "Movie not found!"}
    motion_picture_info = {
        'title': json_data['Title'],
        'description': json_data['Plot'],
        'director': json_data['Director'],
        'actors': json_data['Actors'],
        'writers': json_data['Writer'],
        'genres': json_data['Genre'],
    }
    if json_data['Poster'] != "N/A":
        motion_picture_info['poster'] = json_data['Poster']
    else:
        motion_picture_info['poster'] = None
    
    tmdb_info = get_motion_picture_details_by_name(title)
    if 'Error' in tmdb_info.keys():
        return {"Error": "Movie not found!"}
    motion_picture_info["tmdb_id"] = tmdb_info["tmdb_id"]
    if tmdb_info["type"] == "movie":
        motion_picture_info["type"] = 0
    elif tmdb_info["type"] == "tv":
        motion_picture_info["type"] = 1
    else:
        motion_picture_info["type"] = 2
    
    return motion_picture_info
