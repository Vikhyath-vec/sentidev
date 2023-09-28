-- name: insert_user!
INSERT INTO users (user_email, name) VALUES (:user_email, :name);

-- name: check_user$
SELECT COUNT(*) FROM users WHERE user_email = :user_email;

--name: get_user_by_email^
SELECT user_email, name, points FROM users WHERE user_email = :user_email;

--name: get_user_count$
SELECT COUNT(*) FROM users;