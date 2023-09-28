-- name: insert_movie<!
INSERT INTO motion_picture (title, type, tagline, description, poster, director, tmdb_id) VALUES (:title, 1, :tagline, :description, :poster, :director, :tmdb_id)
ON CONFLICT (title, type) DO NOTHING RETURNING id;

-- name: insert_show<!
INSERT INTO motion_picture (title, type, tagline, description, poster, tmdb_id) VALUES (:title, 2, :tagline, :description, :poster, :tmdb_id)
ON CONFLICT (title, type) DO NOTHING RETURNING id;

-- name: insert_genre<!
INSERT INTO genres (name) VALUES (:name)
ON CONFLICT (name) DO NOTHING RETURNING id;

-- name: insert_actor<!
INSERT INTO actors (name) VALUES (:name)
ON CONFLICT (name) DO NOTHING RETURNING id;

-- name: insert_writer<!
INSERT INTO writers (name) VALUES (:name)
ON CONFLICT (name) DO NOTHING RETURNING id;

--name: insert_motion_picture_genre!
INSERT INTO motion_picture_genres (motion_picture_id, genre_id) VALUES (:motion_picture_id, :genre_id)
ON CONFLICT (motion_picture_id, genre_id) DO NOTHING;

--name: insert_motion_picture_actor!
INSERT INTO motion_picture_actors (motion_picture_id, actor_id) VALUES (:motion_picture_id, :actor_id)
ON CONFLICT (motion_picture_id, actor_id) DO NOTHING;

--name: insert_motion_picture_writer!
INSERT INTO motion_picture_writers (motion_picture_id, writer_id) VALUES (:motion_picture_id, :writer_id)
ON CONFLICT (motion_picture_id, writer_id) DO NOTHING;

--name: get_all_movies
SELECT title, poster, tagline FROM motion_picture WHERE type = 1;

--name: get_all_shows
SELECT title, poster, tagline FROM motion_picture WHERE type = 2;