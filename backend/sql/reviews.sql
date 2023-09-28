-- name: insert_review!
INSERT INTO review (motion_picture_id, title, rating, review, review_date) VALUES (:motion_picture_id, :title, :rating, :review, :review_date);

-- name: add_like!
INSERT INTO likes_and_dislikes (user_email, review_id, like_or_dislike) VALUES (:user_email, :review_id, :like_or_dislike)
ON CONFLICT (user_email, review_id) DO UPDATE SET like_or_dislike = :like_or_dislike;

--name: get_likes$
SELECT COUNT(*) FROM likes_and_dislikes WHERE review_id = :review_id AND like_or_dislike = 1;

--name: get_dislikes$
SELECT COUNT(*) FROM likes_and_dislikes WHERE review_id = :review_id AND like_or_dislike = -1;

--name: get_reviews_count_by_motion_picture$
SELECT COUNT(*) FROM review WHERE motion_picture_id = :motion_picture_id;

--name: get_reviews_by_motion_picture
SELECT * FROM review WHERE motion_picture_id = :motion_picture_id ORDER BY review_date DESC;

--name: get_reviews_by_user
SELECT * FROM review WHERE user_email = :user_email ORDER BY review_date DESC;

-- name: get_review_by_id
SELECT * FROM review WHERE motion_picture_id = :motion_picture_id;

-- name: get_review_by_id_sorted
SELECT rating, review_date FROM review WHERE motion_picture_id = :motion_picture_id ORDER BY review_date;