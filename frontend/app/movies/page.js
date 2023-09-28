"use client"

import React, {useState, useEffect} from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Movies() {
  const router = useRouter();

  const [searchQuery, setSearchQuery] = useState("");
  const [movies, setMovies] = useState([]);
  const [filteredMovies, setFilteredMovies] = useState([]);

  useEffect(() => {
    
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/movies", {method: "GET"});
        const data = await response.json();
        console.log("response:", data);
        setMovies(data);
        setFilteredMovies(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  // Function to handle search input changes
  const handleSearchInputChange = (e) => {
    const query = e.target.value.toLowerCase();
    setSearchQuery(query);

    // Filter movies based on the search query
    const filtered = movies.filter((movie) =>
      movie.title.toLowerCase().includes(query)
    );
    setFilteredMovies(filtered);
  };

  return (
    <div className="bg-gradient-to-b from-gray-900 to-black h-screen">
      <div className="container mx-auto py-8 px-5">
        <Link
          href="/"
          className="bg-blue-500 hover:bg-blue-600 text-white font-semibold mb-5 py-2 px-4 rounded-full transition-transform transform hover:scale-105 inline-block"
        >
          &lt; Back to Home
        </Link>
        <h1 className="text-4xl font-extrabold text-white mb-8">
          Explore Movies
        </h1>

        {/* Search Bar */}
        <div className="relative mb-7">
          <input
            type="text"
            placeholder="Search for movies..."
            value={searchQuery}
            onChange={handleSearchInputChange}
            className="w-full px-4 py-2 pl-10 pr-3 rounded-full bg-gray-800 text-white placeholder-gray-500 focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {searchQuery ? filteredMovies.map((movie) => (
            <button
              className="bg-gray-800 p-4 rounded-lg transition-transform transform hover:scale-105"
              onClick={() => router.push(`/movies/${movie.id}`)}
            >
              <img
                src={movie.poster}
                alt={movie.title}
                className="w-full h-auto rounded-lg"
              />
              <h2 className="text-xl font-semibold text-white py-3">
                {movie.title}
              </h2>
              <p className="text-gray-400 mt-2">{movie.tagline}</p>
            </button>
          )) :
          movies.map((movie) => (
            <button
              className="bg-gray-800 p-4 rounded-lg transition-transform transform hover:scale-105"
              onClick={() => router.push(`/movies/${movie.id}`)}
            >
              <img
                src={movie.poster}
                alt={movie.title}
                className="w-full h-auto rounded-lg"
              />
              <h2 className="text-xl font-semibold text-white py-3">
                {movie.title}
              </h2>
              <p className="text-gray-400 mt-2">{movie.tagline}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
