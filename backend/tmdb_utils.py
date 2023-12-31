import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

def get_motion_picture_details_by_name(title: str) -> dict:
    url = "https://api.themoviedb.org/3/search/multi?query={}&include_adult=true&language=en-US&page=1".format(title)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(TMDB_ACCESS_TOKEN)
    }
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    if json_data["total_results"] == 0:
        return {"Error": "Movie not found!"}

    return_info = {
        "tmdb_id": json_data["results"][0]["id"],
        "type": json_data["results"][0]["media_type"]
    }

    return return_info

def get_actor_profile_picture(name: str) -> str:
    url = "https://api.themoviedb.org/3/search/person?query={}&include_adult=true&language=en-US&page=1".format(name)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(TMDB_ACCESS_TOKEN)
    }

    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    if json_data["total_results"] == 0:
        return {"Error": "Actor not found!"}
    
    actor_url = "https://image.tmdb.org/t/p/original" + json_data["results"][0]["profile_path"]
    return actor_url

def get_recommendations(tmdb_id, mtype):
    if mtype == 1:
        url = "https://api.themoviedb.org/3/movie/{}/recommendations?language=en-US&page=1".format(tmdb_id)
    elif mtype == 2:
        url = "https://api.themoviedb.org/3/tv/{}/recommendations?language=en-US&page=1".format(tmdb_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(TMDB_ACCESS_TOKEN)
    }

    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    recommendations = []
    if json_data["total_results"] == 0:
        return {"Error": "No recommendations found!"}
    elif json_data["total_results"] < 5:
        for rec in json_data["results"]:
            if mtype == 1:
                recommendations.append(rec["title"])
            elif mtype == 2:
                recommendations.append(rec["name"])
    else:
        for rec in json_data["results"][:5]:
            if mtype == 1:
                recommendations.append(rec["title"])
            elif mtype == 2:
                recommendations.append(rec["name"])
    return recommendations