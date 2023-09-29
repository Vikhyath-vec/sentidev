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
INSERT INTO actors (name, profile_picture) VALUES (:name, :profile_picture)
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
SELECT id, title, poster, tagline FROM motion_picture WHERE type = 1;

--name: get_all_shows
SELECT id, title, poster, tagline FROM motion_picture WHERE type = 2;

--name: get_movie_by_id^
SELECT id, title, poster, tagline, description, director, tmdb_id FROM motion_picture WHERE id = :id AND type = 1;

--name: get_show_by_id^
SELECT id, title, poster, tagline, description, tmdb_id FROM motion_picture WHERE id = :id AND type = 2;

--name: get_genres_by_motion_picture_id
SELECT genres.id, genres.name FROM genres INNER JOIN motion_picture_genres ON genres.id = motion_picture_genres.genre_id WHERE motion_picture_genres.motion_picture_id = :id;

--name: get_actors_by_motion_picture_id
SELECT actors.id, actors.name, actors.profile_picture FROM actors INNER JOIN motion_picture_actors ON actors.id = motion_picture_actors.actor_id WHERE motion_picture_actors.motion_picture_id = :id;

--name: get_writers_by_motion_picture_id
SELECT writers.id, writers.name FROM writers INNER JOIN motion_picture_writers ON writers.id = motion_picture_writers.writer_id WHERE motion_picture_writers.motion_picture_id = :id;

-- name: get_actor_id^
SELECT id FROM actors WHERE name = :name;

-- name: get_writer_id^
SELECT id FROM writers WHERE name = :name;

-- name: get_genre_id^
SELECT id FROM genres WHERE name = :name;

-- name: get_motion_picture_id^
SELECT id FROM motion_picture WHERE title = :title AND type = :mtype;

-- name: get_generic_motion_picture_id^
SELECT id FROM motion_picture WHERE title = :title;

-- name: check_recommendation_exists$
SELECT COUNT(*) FROM recommendations WHERE motion_picture_id = :motion_picture_id;

-- name: insert_recommendation!
INSERT INTO recommendations (motion_picture_id, recommended_motion_picture_id) VALUES (:motion_picture_id, :recommended_motion_picture_id);

-- name: get_recommendations_by_motion_picture_id
SELECT motion_picture.id, motion_picture.title, motion_picture.poster, motion_picture.tagline FROM motion_picture INNER JOIN recommendations ON motion_picture.id = recommendations.recommended_motion_picture_id WHERE recommendations.motion_picture_id = :id;