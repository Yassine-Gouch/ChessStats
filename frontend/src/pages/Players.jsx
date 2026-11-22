import { useState } from "react";

import { Link } from "react-router-dom";

import { searchPlayers } from "../services/api";

function Players() {

  const [query, setQuery] = useState("");

  const [players, setPlayers] = useState([]);

  const [loading, setLoading] = useState(false);

  async function handleSearch() {

    if (!query.trim()) return;

    setLoading(true);

    try {

      const results = await searchPlayers(query);

      setPlayers(results);

    } catch (error) {

      console.error(error);

    }

    setLoading(false);

  }

  return (

    <div className="max-w-7xl">

      {/* HEADER */}

      <div className="mb-12">

        <span
          className="
            inline-flex
            items-center
            px-4
            py-2
            rounded-full
            text-sm
            font-medium
            bg-blue-500/10
            text-blue-400
            border
            border-blue-500/20
            mb-6
          "
        >
          👤 Players Database
        </span>

        <h1
          className="
            text-5xl
            font-bold
            text-white
            mb-4
          "
        >
          Search Players
        </h1>

        <p
          className="
            text-slate-400
            text-xl
          "
        >
          Explore player profiles,
          ratings and chess statistics.
        </p>

      </div>

      {/* SEARCH */}

      <div
        className="
          bg-slate-900
          border
          border-slate-800
          rounded-2xl
          p-6
          mb-10
        "
      >

        <label
          className="
            block
            text-slate-300
            text-sm
            mb-3
          "
        >
          Search a player
        </label>

        <div className="flex gap-4">

          <input
            type="text"
            value={query}
            onChange={(e) =>
              setQuery(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSearch();
              }
            }}
            placeholder="Magnus Carlsen..."
            className="
              flex-1
              px-4
              py-4
              rounded-xl
              bg-slate-950
              border
              border-slate-700
              text-white
              outline-none
              focus:border-blue-500
            "
          />

          <button
            onClick={handleSearch}
            className="
              px-6
              bg-blue-600
              hover:bg-blue-700
              rounded-xl
              text-white
              font-semibold
              transition
            "
          >
            Search
          </button>

        </div>

      </div>

      {/* LOADING */}

      {loading && (

        <div className="text-slate-400">
          Searching...
        </div>

      )}

      {/* RESULTS */}

      {!loading && players.length > 0 && (

        <div className="grid grid-cols-2 gap-6">

          {players.map((player) => (

            <Link
              key={player.fideid}
              to={`/player/${player.name.split(",")[0]}`}
            >

              <div
                className="
                  bg-slate-900
                  border
                  border-slate-800
                  rounded-2xl
                  p-6
                  hover:border-blue-500
                  hover:-translate-y-1
                  hover:shadow-lg
                  hover:shadow-blue-500/10
                  transition-all
                  duration-300
                  cursor-pointer
                "
              >

                <h2
                  className="
                    text-white
                    text-xl
                    font-bold
                    mb-2
                  "
                >
                  {player.name}
                </h2>

                <p className="text-slate-400">

                  {player.title || "Player"}

                  {" • "}

                  {player.country}

                </p>

                <div className="mt-5">

                  <p className="text-slate-400 text-sm">
                    Rating
                  </p>

                  <p
                    className="
                      text-blue-400
                      text-2xl
                      font-bold
                    "
                  >
                    {player.rating}
                  </p>

                </div>

              </div>

            </Link>

          ))}

        </div>

      )}

      {/* EMPTY STATE */}

      {!loading &&
        players.length === 0 && (

        <div
          className="
            bg-slate-900
            border
            border-slate-800
            rounded-2xl
            p-10
            text-center
          "
        >

          <div className="text-5xl mb-4">
            ♟️
          </div>

          <h2
            className="
              text-white
              text-2xl
              font-bold
              mb-3
            "
          >
            Search for a player
          </h2>

          <p className="text-slate-400">

            Enter a player name
            and click Search.

          </p>

        </div>

      )}

    </div>

  );

}

export default Players;
