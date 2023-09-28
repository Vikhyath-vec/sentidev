import React from "react";
import Link from "next/link";

const showsData = [
  {
    title: "TV Show 1",
    description: "Description for TV Show 1",
  },
  {
    title: "TV Show 2",
    description: "Description for TV Show 2",
  },
  {
    title: "TV Show 3",
    description: "Description for TV Show 3",
  },
];

export default function Shows() {
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
          Explore TV Shows
        </h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {showsData.map((shows, index) => (
            <div key={index} className="bg-gray-800 p-4 rounded-lg">
              <h2 className="text-xl font-semibold text-white">
                {shows.title}
              </h2>
              <p className="text-gray-400 mt-2">{shows.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
