import Link from "next/link";

export default function Home() {
  return (
    <div
      className="bg-gradient-to-b from-gray-900 to-black h-screen flex flex-col justify-center items-center"
      style={{
        backgroundImage: `url('/bg_1.jpeg')`,
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        // backgroundPosition: "center",
        // backgroundColor: "rgba(0, 0, 0, 0.7)",
      }}
    >
      <h1 className="text-6xl font-extrabold text-white mb-8">
        Review Platform
      </h1>
      <div className="flex space-x-4">
        <Link href="/movies">
          <button className="bg-red-700 hover:bg-red-800 transition-transform transform hover:scale-105 text-white font-semibold py-3 px-6 rounded-full">
            Explore Movies
          </button>
        </Link>
        <Link href="/tv-shows">
          <button className="bg-blue-700 hover:bg-blue-800 transition-transform transform hover:scale-105 text-white font-semibold py-3 px-6 rounded-full">
            Explore TV Shows
          </button>
        </Link>
      </div>
    </div>
  );
}
