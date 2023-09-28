import aiosql

queries = aiosql.from_path("sql", "psycopg2")

def get_all_details(conn, id1, mtype):
    if mtype == 1:
        motion_picture_info = queries.get_movie_by_id(conn, id=id1)
    elif mtype == 2:
        motion_picture_info = queries.get_show_by_id(conn, id=id1)

    genres_info = queries.get_genres_by_motion_picture_id(conn, id=id1)
    actors_info = queries.get_actors_by_motion_picture_id(conn, id=id1)
    writers_info = queries.get_writers_by_motion_picture_id(conn, id=id1)
    movie_dict = {
        "id": motion_picture_info[0],
        "title": motion_picture_info[1],
        "poster": motion_picture_info[2],
        "tagline": motion_picture_info[3],
        "desc": motion_picture_info[4],
    }
    if mtype == 1:
        movie_dict["director"] = motion_picture_info[5]
    genres = []
    for genre in genres_info:
        genres.append(genre[1])
    movie_dict["genres"] = genres
    writers = []
    for writer in writers_info:
        writers.append(writer[1])
    movie_dict["writers"] = writers
    actors = []
    for actor in actors_info:
        actor_dict = {
            "name": actor[1],
            "profilePicture": actor[2]
        }
        actors.append(actor_dict)
    movie_dict["actors"] = actors
    reviews = []
    reviews_info = queries.get_review_by_id(conn, motion_picture_id=motion_picture_info[0])
    for review in reviews_info[:5]:
        likes = queries.get_likes(conn, review_id=review[0])
        dislikes = queries.get_dislikes(conn, review_id=review[0])
        review_dict = {
            "id": review[0],
            "title": review[3],
            "text": review[5],
            "rating": review[4],
            "date": review[6],
            "likes": likes,
            "dislikes": dislikes
        }
        reviews.append(review_dict)
    movie_dict["reviews"] = reviews
    return movie_dict
