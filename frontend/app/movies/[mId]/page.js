"use client";

import Link from "next/link";
import React, { useState, useEffect } from "react";
import axios from "axios";

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

export default function MovieDetails({ params }) {

  console.log("params:", params);

  const [movieData, setMovieData] = useState([]);
  const [reviewData, setReviewData] = useState({
    mid: params.mId,
    title: "",
    review: "",
    rating: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/movies/${params.mId}`);
        console.log("response:", response.data);
        setMovieData(response.data);
        setLoading(false);
      } catch (error) {
        setLoading(false);
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  if(loading) {
    return <div>Loading...</div>
  }

  const handleReviewInputChange = (e) => {
    const { name, value } = e.target;
    setReviewData({ ...reviewData, [name]: value });
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        `http://localhost:8000/add_review`,
        reviewData
      );

      console.log("Review submitted successfully:", response.data);

      setReviewData({
        title: "",
        review: "",
        rating: 0,
      });
    } catch (error) {
      console.error("Error submitting review:", error);
    }
  };

  const percentage = (movieData.overallRating / 10) * 100;

  return (
    <div className="bg-gradient-to-b from-gray-900 to-black min-h-screen text-white">
      <Link
        href="/movies"
        className="bg-blue-500 hover:bg-blue-600 text-white font-semibold mt-5 mb-0 ml-5 py-2 px-4 rounded-full transition-transform transform hover:scale-105 inline-block"
      >
        &lt; Back to Movies
      </Link>

      <div className="container mx-auto p-4 flex">
        {/* Poster */}
        <div className="flex-shrink-0 w-1/3">
          <img
            src={movieData.poster} // Replace with the actual URL of the movie poster
            alt={movieData.title}
            className="rounded-lg shadow-lg"
          />
        </div>

        {/* Movie Details */}
        <div className="flex-grow ml-4">
          <h1 className="text-4xl font-semibold mb-2">{movieData.title}</h1>
          <p className="text-lg">{movieData.tagline}</p>

          {/* Summary */}
          <div className="mt-4">
            <h2 className="text-2xl font-semibold">Summary</h2>
            <p>{movieData.desc}</p>
          </div>

          {/* Director */}
          <div className="mt-4">
            <h2 className="text-2xl font-semibold">Director</h2>
            <p>{movieData.director}</p>
          </div>

          {/* Writers */}
          <div className="mt-4">
            <h2 className="text-2xl font-semibold">Writers</h2>
            <p>{movieData.writers.join(", ")}</p>
          </div>

          {/* Actors */}
          <div className="mt-4">
            <h2 className="text-2xl font-semibold">Actors</h2>
            <div className="flex flex-wrap gap-4">
              {movieData.actors.map((actor) => (
                <div key={actor.name} className="text-center">
                  <img
                    src={actor.profilePicture}
                    alt={actor.name}
                    className="w-32 h-32 object-cover rounded-full mx-auto mb-2"
                  />
                  <p className="text-sm">{actor.name}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Genre */}
          <div className="mt-4">
            <h2 className="text-2xl font-semibold">Genres</h2>
            <p>{movieData.genres.join(", ")}</p>
          </div>
        </div>
      </div>

      {/* Reviews */}
      <div className="mt-8 mr-5 ml-5">
        <div className="bg-gray-800 rounded-lg p-4 mb-4">
          <h3 className="text-xl font-semibold text-yellow-400">
            Overall Review
          </h3>
          <p className="text-lg mt-2">
            {movieData.overallReview || "No overall review available."}
          </p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4 mb-4">
          <h3 className="text-xl font-semibold text-yellow-400">
            Overall Rating
          </h3>
          {/* <p className="text-lg mt-2">
            {movieData.overallRating || "No overall rating available."} / 10
          </p> */}
          <div className="container mx-auto py-8 px-4">
          <div className="w-full bg-gray-900 h-8 rounded-full overflow-hidden">
            <div
              className="h-8 rounded-full transition-all ease-in-out duration-500"
              style={{
                width: `${percentage}%`,
                background: "linear-gradient(to right, #3182ce, #63b3ed)",
              }}
            ></div>
          </div>
          <div className="mt-2 text-white text-center">
            {movieData.overallRating.toFixed(2)} / 10
          </div>
        </div>
        </div>        

        <h2 className="text-3xl font-semibold mb-4">Top Reviews</h2>

        {movieData.reviews.map((review, index) => (
          <div key={index} className="bg-gray-800 rounded-lg p-4 mt-4">
            {/* Review Title */}
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-semibold">{review.title}</h3>
              <p className="text-sm text-gray-400">{review.date}</p>
            </div>

            {/* Review Text */}
            <p className="text-lg mt-2">{review.text}</p>

            {/* Rating */}
            <div className="mb-2 flex items-center">
              <span className="text-xl font-semibold mr-2">Rating:</span>
              <span className="text-xl">{review.rating}</span>
            </div>

            {/* Likes and Dislikes */}
            <div className="flex items-center mt-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-6 h-6 mr-2"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M6.633 10.5c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 012.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 00.322-1.672V3a.75.75 0 01.75-.75A2.25 2.25 0 0116.5 4.5c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 01-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 00-1.423-.23H5.904M14.25 9h2.25M5.904 18.75c.083.205.173.405.27.602.197.4-.078.898-.523.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 01-.521-3.507c0-1.553.295-3.036.831-4.398C3.387 10.203 4.167 9.75 5 9.75h1.053c.472 0 .745.556.5.96a8.958 8.958 0 00-1.302 4.665c0 1.194.232 2.333.654 3.375z"
                />
              </svg>
              {review.likes}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-6 h-6 ml-4 mr-2"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M7.5 15h2.25m8.024-9.75c.011.05.028.1.052.148.591 1.2.924 2.55.924 3.977a8.96 8.96 0 01-.999 4.125m.023-8.25c-.076-.365.183-.75.575-.75h.908c.889 0 1.713.518 1.972 1.368.339 1.11.521 2.287.521 3.507 0 1.553-.295 3.036-.831 4.398C20.613 14.547 19.833 15 19 15h-1.053c-.472 0-.745-.556-.5-.96a8.95 8.95 0 00.303-.54m.023-8.25H16.48a4.5 4.5 0 01-1.423-.23l-3.114-1.04a4.5 4.5 0 00-1.423-.23H6.504c-.618 0-1.217.247-1.605.729A11.95 11.95 0 002.25 12c0 .434.023.863.068 1.285C2.427 14.306 3.346 15 4.372 15h3.126c.618 0 .991.724.725 1.282A7.471 7.471 0 007.5 19.5a2.25 2.25 0 002.25 2.25.75.75 0 00.75-.75v-.633c0-.573.11-1.14.322-1.672.304-.76.93-1.33 1.653-1.715a9.04 9.04 0 002.86-2.4c.498-.634 1.226-1.08 2.032-1.08h.384"
                />
              </svg>
              {review.dislikes}
            </div>
          </div>
        ))}
      </div>

      {/* Review Form */}
      <div className="mt-8">
        <h2 className="text-3xl font-semibold mb-4">Add a Review</h2>
        <form
          onSubmit={handleReviewSubmit}
          className="bg-gray-800 rounded-lg p-6"
        >
          <div className="mb-4">
            <label htmlFor="title" className="block text-lg text-white mb-2">
              Title
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={reviewData.title}
              onChange={handleReviewInputChange}
              className="w-full px-4 py-2 text-lg bg-gray-700 rounded-lg focus:outline-none focus:ring focus:border-blue-300"
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="text" className="block text-lg text-white mb-2">
              Review
            </label>
            <textarea
              type="text"
              id="review"
              name="review"
              value={reviewData.review}
              onChange={handleReviewInputChange}
              rows="4"
              className="w-full px-4 py-2 text-lg bg-gray-700 rounded-lg focus:outline-none focus:ring focus:border-blue-300"
              required
            ></textarea>
          </div>
          <div className="mb-4">
            <label htmlFor="rating" className="block text-lg text-white mb-2">
              Rating
            </label>
            <input
              type="number"
              id="rating"
              name="rating"
              value={reviewData.rating}
              onChange={handleReviewInputChange}
              min="1"
              max="10"
              className="w-16 px-4 py-2 text-lg bg-gray-700 rounded-lg focus:outline-none focus:ring focus:border-blue-300"
              required
            />
          </div>
          <div>
            <button
              type="submit"
              className="bg-blue-700 hover:bg-blue-800 text-white font-semibold py-3 px-6 rounded-full"
            >
              Submit Review
            </button>
          </div>
        </form>
      </div>

      <div className="mt-8 ml-5">
        <h2 className="text-3xl font-semibold mb-4">
          Average Rating over Time
        </h2>
        <div className="flex justify-center items-center">
          <img
            src={`data:image/png;base64,${movieData.runningAverage}`}
            alt="worldcloud"
            className="w-1/2 h-full rounded-lg shadow-lg"
          />
        </div>
      </div>

      <div className="mt-8 ml-5 mb-5">
        <h2 className="text-3xl font-semibold mb-4">Word Cloud</h2>
        <div className="flex justify-center items-center">
          <img
            src={`data:image/png;base64,${movieData.wordcloud}`}
            alt="worldcloud"
            className="w-1/2 h-full rounded-lg shadow-lg"
          />
        </div>
      </div>

      {/* Ratings Table */}
      {/* <div className="container mx-auto py-8 px-4">
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
      </div> */}

      {/* Recommended Movies */}
      {/* <div className="container mx-auto py-8 px-4">
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
      </div> */}
    </div>
  );
}