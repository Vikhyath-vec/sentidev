-- name: create_schema#
CREATE TABLE users
(
  user_email VARCHAR NOT NULL PRIMARY KEY,
  name VARCHAR NOT NULL,
  points INT NOT NULL DEFAULT 0
);

CREATE TABLE motion_picture
(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    title VARCHAR NOT NULL,
    type INT NOT NULL,
    tagline VARCHAR,
    description VARCHAR NOT NULL,
    poster VARCHAR,
    director VARCHAR,
    tmdb_id BIGINT NOT NULL UNIQUE,
    UNIQUE (title, type)
);

CREATE TABLE writers
(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE motion_picture_writers
(
    motion_picture_id BIGINT NOT NULL,
    writer_id BIGINT NOT NULL,
    PRIMARY KEY (motion_picture_id, writer_id),
    FOREIGN KEY (motion_picture_id) REFERENCES motion_picture(id),
    FOREIGN KEY (writer_id) REFERENCES writers(id)
);

CREATE TABLE genres
(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE motion_picture_genres
(
    motion_picture_id BIGINT NOT NULL,
    genre_id BIGINT NOT NULL,
    PRIMARY KEY (motion_picture_id, genre_id),
    FOREIGN KEY (motion_picture_id) REFERENCES motion_picture(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);

CREATE TABLE actors
(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE motion_picture_actors
(
    motion_picture_id BIGINT NOT NULL,
    actor_id BIGINT NOT NULL,
    PRIMARY KEY (motion_picture_id, actor_id),
    FOREIGN KEY (motion_picture_id) REFERENCES motion_picture(id),
    FOREIGN KEY (actor_id) REFERENCES actors(id)
);

CREATE TABLE review
(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    user_email VARCHAR NOT NULL,
    motion_picture_id BIGINT NOT NULL,
    title VARCHAR NOT NULL,
    rating INT NOT NULL,
    review VARCHAR NOT NULL,
    review_date DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_email) REFERENCES users(user_email),
    FOREIGN KEY (motion_picture_id) REFERENCES motion_picture(id)
);

CREATE TABLE likes_and_dislikes
(
    user_email VARCHAR NOT NULL,
    review_id BIGINT NOT NULL,
    like_or_dislike INT NOT NULL,
    like_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_email, review_id),
    FOREIGN KEY (user_email) REFERENCES users(user_email),
    FOREIGN KEY (review_id) REFERENCES review(id)
);
