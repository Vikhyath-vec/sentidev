"use client";

import Link from "next/link";
import React, { useState } from "react";

const movieData = {
  id: 1,
  title: "Interstellar",
  description: "Space Adventure!",
  image: "/mv_1.jpg",
  ratings: 4,
  reviews: [
    {
      id: 1,
      user: "Steve",
      comment: "Great movie! Highly recommended.",
      rating: 4,
    },
    {
      id: 2,
      user: "Stephen",
      comment: "Enjoyed every minute of it.",
      rating: 4,
    },
  ],
};

const recommendedMovies = [
  {
    id: 2,
    title: "Inception",
    image: "/mv_2.jpg",
  },
  {
    id: 3,
    title: "Batman",
    image: "/mv_3.jpg",
  },
];

export default function MovieDetails() {
  const [userReview, setUserReview] = useState("");
  const [userRating, setUserRating] = useState(0);
  const [ratingsData, setRatingsData] = useState({
    5: 0, // Number of 5-star ratings
    4: 0, // Number of 4-star ratings
    3: 0, // Number of 3-star ratings
    2: 0, // Number of 2-star ratings
    1: 0, // Number of 1-star ratings
  });

  const handleReviewChange = (e) => {
    setUserReview(e.target.value);
  };

  const handleRatingChange = (rating) => {
    setUserRating(rating);
  };

  const handleAddReview = () => {
    if (userReview.trim() !== "" && userRating > 0) {
      // Add the user's review and rating
      movieData.reviews.push({
        id: movieData.reviews.length + 1,
        user: "Your Name", // Replace with user's name or use a user authentication system
        comment: userReview,
        rating: userRating,
      });

      // Update the ratings data
      setRatingsData((prevData) => ({
        ...prevData,
        [userRating]: prevData[userRating] + 1,
      }));

      // Clear the textarea and reset the rating
      setUserReview("");
      setUserRating(0);
    }
  };

  // Calculate the average rating
  const totalRatings = Object.values(ratingsData).reduce((acc, curr) => acc + curr, 0);
  const totalPoints = Object.entries(ratingsData).reduce((acc, [rating, count]) => acc + rating * count, 0);
  const averageRating = totalPoints / totalRatings || movieData.ratings;
  const percentage = (averageRating / 5) * 100;

  return (
    <div className="bg-gradient-to-b from-gray-900 to-black min-h-screen">
      <Link
        href="/movies"
        className="bg-blue-500 hover:bg-blue-600 text-white font-semibold mt-5 mb-0 ml-5 py-2 px-4 rounded-full transition-transform transform hover:scale-105 inline-block"
      >
        &lt; Back to Movies
      </Link>
      {/* Movie Details */}
      <div className="container mx-auto py-8 px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="max-h-screen overflow-hidden">
            <img
              src={movieData.image}
              alt={movieData.title}
              className="max-w-full w-3/5 h-auto rounded-lg"
            />
          </div>
          <div>
            <h1 className="text-4xl font-extrabold text-white mb-4">
              {movieData.title}
            </h1>
            <p className="text-gray-400 mb-4">{movieData.description}</p>
            <div className="flex items-center">
              <span className="text-yellow-400 text-lg font-semibold">
                {averageRating.toFixed(1)}
              </span>
              <span className="text-gray-400 ml-2">
                ({movieData.reviews.length} Reviews)
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Reviews */}
      <div className="container mx-auto py-8 px-4">
        <h2 className="text-2xl font-extrabold text-white mb-4">Reviews</h2>
        <ul className="divide-y divide-gray-600">
          {movieData.reviews.map((review) => (
            <li key={review.id} className="py-4">
              <div className="text-white font-semibold">{review.user}</div>
              <div className="text-gray-400 mt-1">{review.comment}</div>
            </li>
          ))}
        </ul>
      </div>

      {/* Add Your Review */}
      <div className="container mx-auto py-8 px-4">
        <h2 className="text-2xl font-extrabold text-white mb-4">
          Add Your Review
        </h2>
        <div className="rounded-lg bg-gray-800 p-4">
          <textarea
            className="w-full h-32 px-4 py-2 rounded-lg text-gray-100 bg-gray-700 focus:outline-none focus:ring focus:border-blue-500"
            placeholder="Write your review here..."
            value={userReview}
            onChange={handleReviewChange}
          />
          <div className="flex justify-between items-center mt-4">
            <div className="flex items-center space-x-2">
              <span className="text-white font-semibold text-lg">
                Your Rating:
              </span>
              <div className="flex space-x-2">
                {[1, 2, 3, 4, 5].map((rating) => (
                  <button
                    key={rating}
                    className={`${
                      userRating >= rating ? "text-yellow-400" : "text-gray-400"
                    } text-2xl focus:outline-none focus:text-yellow-400`}
                    onClick={() => handleRatingChange(rating)}
                  >
                    &#9733;
                  </button>
                ))}
              </div>
            </div>
            <button
              onClick={handleAddReview}
              className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-full transition-transform transform hover:scale-105"
            >
              Submit Review
            </button>
          </div>
        </div>
      </div>

      {/* Horizontal Rating Bar */}
      <div className="container mx-auto py-8 px-4">
        <h2 className="text-2xl font-extrabold text-white mb-4">
          Average Rating
        </h2>
        <div className="w-full bg-gray-800 h-8 rounded-full overflow-hidden">
          <div
            className="h-8 rounded-full transition-all ease-in-out duration-500"
            style={{
              width: `${percentage}%`,
              background: "linear-gradient(to right, #3182ce, #63b3ed)",
            }}
          ></div>
        </div>
        <div className="mt-2 text-white text-center">
          {averageRating.toFixed(1)}
        </div>
      </div>

      {/* Ratings Table */}
      <div className="container mx-auto py-8 px-4">
        <h2 className="text-2xl font-extrabold text-white mb-4">
          Ratings Summary
        </h2>
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th className="text-left text-gray-400">Rating</th>
              <th className="text-left text-gray-400">Number of Ratings</th>
            </tr>
          </thead>
          <tbody>
            {[5, 4, 3, 2, 1].map((rating) => (
              <tr key={rating}>
                <td className="text-white">{rating} Star</td>
                <td className="text-white">{ratingsData[rating]}</td>
              </tr>
            ))}
            <tr>
              <td className="text-white font-semibold">Average Rating</td>
              <td className="text-yellow-400 font-semibold">
                {averageRating.toFixed(1)}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Recommended Movies */}
      <div className="container mx-auto py-8 px-4">
        <h2 className="text-2xl font-extrabold text-white mb-4">
          Recommended Movies
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {recommendedMovies.map((movie) => (
            <div
              key={movie.id}
              className="bg-gray-800 p-4 rounded-lg transition-transform transform hover:scale-105 relative"
            >
              <img
                src={movie.image}
                alt={movie.title}
                className="w-full h-auto rounded-lg"
              />
              <h2 className="text-lg font-semibold text-white mt-2">
                {movie.title}
              </h2>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}