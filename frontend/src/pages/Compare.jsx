import { useState } from "react";
import RatingComparisonChart
from "../components/RatingComparisonChart";

function Compare() {

  const [playerA, setPlayerA] = useState("");
  const [playerB, setPlayerB] = useState("");

  const [selectedPlayerA, setSelectedPlayerA] =
    useState(null);

  const [selectedPlayerB, setSelectedPlayerB] =
    useState(null);

  const [suggestionsA, setSuggestionsA] =
    useState([]);

  const [suggestionsB, setSuggestionsB] =
    useState([]);

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [ratingChart, setRatingChart] =
  useState([]);

  async function handleSearchA(value) {

    setPlayerA(value);

    setSelectedPlayerA(null);

    if (value.length < 2) {

      setSuggestionsA([]);

      return;

    }

    try {

      const response = await fetch(
        `https://chessstats-jwakvg.fly.dev/players/search?q=${value}`
      );

      const data = await response.json();

      setSuggestionsA(data);

    } catch (error) {

      console.error(error);

    }

  }

  async function handleSearchB(value) {

    setPlayerB(value);

    setSelectedPlayerB(null);

    if (value.length < 2) {

      setSuggestionsB([]);

      return;

    }

    try {

      const response = await fetch(
        `https://chessstats-jwakvg.fly.dev/players/search?q=${value}`
      );

      const data = await response.json();

      setSuggestionsB(data);

    } catch (error) {

      console.error(error);

    }

  }

  async function handleCompare() {

    if (
      !selectedPlayerA ||
      !selectedPlayerB
    ) {

      alert(
        "Select players from suggestions."
      );

      return;

    }

    setLoading(true);

    try {

      const response = await fetch(
        `https://chessstats-jwakvg.fly.dev/players/compare/${playerA}/${playerB}`
      );

      const data = await response.json();

      setResult(data);
      const historyAResponse =
  await fetch(
    `https://chessstats-jwakvg.fly.dev/players/rating-history/${playerA}`
  );

const historyA =
  await historyAResponse.json();

const historyBResponse =
  await fetch(
    `https://chessstats-jwakvg.fly.dev/players/rating-history/${playerB}`
  );

const historyB =
  await historyBResponse.json();
  const cleanHistoryB =
  historyB.filter(
    item => item.rating > 2500
  );
  const mergedData =
  historyA.map((item, index) => ({

    date: item.date,

    playerA: item.rating,

    playerB:
      cleanHistoryB[index]?.rating ?? null

  }));

setRatingChart(
  mergedData
);

    } catch (error) {

      console.error(error);

    }

    setLoading(false);

  }

  const winner =
    result
      ? (
          result.player_a.rating >
          result.player_b.rating
        )
          ? "a"
          : "b"
      : null;

  return (

    <div className="max-w-7xl">

      <div className="mb-10">

        <h1
          className="
            text-5xl
            font-bold
            text-white
            mb-4
          "
        >
          Player Comparison
        </h1>

        <p
          className="
            text-slate-400
            text-xl
          "
        >
          Compare ratings, games,
          elo history and head-to-head.
        </p>

      </div>

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

        <div className="grid grid-cols-2 gap-4">

          {/* PLAYER A */}

          <div className="relative">

            <input
              type="text"
              placeholder="Magnus..."
              value={playerA}
              onChange={(e) =>
                handleSearchA(
                  e.target.value
                )
              }
              className="
                w-full
                bg-slate-950
                border
                border-slate-700
                rounded-xl
                px-4
                py-4
                text-white
                outline-none
                focus:border-blue-500
              "
            />

            {suggestionsA.length > 0 && (

              <div
                className="
                  absolute
                  z-50
                  mt-2
                  w-full
                  bg-slate-950
                  border
                  border-slate-700
                  rounded-xl
                  overflow-hidden
                "
              >

                {suggestionsA.map(
                  (player) => (

                    <div
                      key={player.fideid}
                      onClick={() => {

                        setPlayerA(
                          player.name
                        );

                        setSelectedPlayerA(
                          player
                        );

                        setSuggestionsA([]);

                      }}
                      className="
                        px-4
                        py-3
                        cursor-pointer
                        text-white
                        hover:bg-slate-800
                      "
                    >

                      {player.name}

                    </div>

                  )
                )}

              </div>

            )}

            {selectedPlayerA && (

              <div
                className="
                  mt-2
                  text-green-400
                  text-sm
                "
              >
                ✅ Selected:
                {" "}
                {selectedPlayerA.name}
              </div>

            )}

          </div>

          {/* PLAYER B */}
                    <div className="relative">

            <input
              type="text"
              placeholder="Hikaru..."
              value={playerB}
              onChange={(e) =>
                handleSearchB(
                  e.target.value
                )
              }
              className="
                w-full
                bg-slate-950
                border
                border-slate-700
                rounded-xl
                px-4
                py-4
                text-white
                outline-none
                focus:border-blue-500
              "
            />

            {suggestionsB.length > 0 && (

              <div
                className="
                  absolute
                  z-50
                  mt-2
                  w-full
                  bg-slate-950
                  border
                  border-slate-700
                  rounded-xl
                  overflow-hidden
                "
              >

                {suggestionsB.map(
                  (player) => (

                    <div
                      key={player.fideid}
                      onClick={() => {

                        setPlayerB(
                          player.name
                        );

                        setSelectedPlayerB(
                          player
                        );

                        setSuggestionsB([]);

                      }}
                      className="
                        px-4
                        py-3
                        cursor-pointer
                        text-white
                        hover:bg-slate-800
                      "
                    >

                      {player.name}

                    </div>

                  )
                )}

              </div>

            )}

            {selectedPlayerB && (

              <div
                className="
                  mt-2
                  text-green-400
                  text-sm
                "
              >
                ✅ Selected:
                {" "}
                {selectedPlayerB.name}
              </div>

            )}

          </div>

        </div>

        <button
          onClick={handleCompare}
          className="
            mt-6
            px-8
            py-3
            rounded-xl
            bg-blue-600
            hover:bg-blue-700
            text-white
            font-semibold
          "
        >
          Compare
        </button>

      </div>

      {loading && (

        <div className="text-slate-400">
          Loading...
        </div>

      )}

      {result && (

        <div className="space-y-8">

          <div className="grid grid-cols-2 gap-6">

            <div
              className={`
                bg-slate-900
                border
                rounded-2xl
                p-6
                ${
                  winner === "a"
                    ? "border-yellow-500"
                    : "border-slate-800"
                }
              `}
            >

              <h2
                className="
                  text-white
                  text-2xl
                  font-bold
                  mb-4
                "
              >
                {winner === "a" && "🏆 "}
                {result.player_a.name}
              </h2>

              <div className="space-y-3 text-slate-300">

                <p>
                  ⭐ Rating: {result.player_a.rating}
                </p>

                <p>
                  🎮 Games:
                  {" "}
                  {result.player_a.games || "—"}
                </p>

                <p>
                  📈 Last Elo:
                  {" "}
                  {result.player_a.last_elo || "—"}
                </p>

                <p>
                  🌍 {result.player_a.country}
                </p>

              </div>

            </div>

            <div
              className={`
                bg-slate-900
                border
                rounded-2xl
                p-6
                ${
                  winner === "b"
                    ? "border-yellow-500"
                    : "border-slate-800"
                }
              `}
            >

              <h2
                className="
                  text-white
                  text-2xl
                  font-bold
                  mb-4
                "
              >
                {winner === "b" && "🏆 "}
                {result.player_b.name}
              </h2>

              <div className="space-y-3 text-slate-300">

                <p>
                  ⭐ Rating: {result.player_b.rating}
                </p>

                <p>
                  🎮 Games:
                  {" "}
                  {result.player_b.games || "—"}
                </p>

                <p>
                  📈 Last Elo:
                  {" "}
                  {result.player_b.last_elo || "—"}
                </p>

                <p>
                  🌍 {result.player_b.country}
                </p>

              </div>

            </div>

          </div>

          <div
            className={`
              bg-slate-900
              border
              rounded-2xl
              p-6
              ${
                winner === "b"
                  ? "border-yellow-500"
                  : "border-slate-800"
              }
            `}
          >

            <h2
              className="
                text-white
                text-3xl
                font-bold
                mb-6
              "
            >
              ⚔ Comparison Summary
            </h2>
<div className="grid grid-cols-2 gap-8">

  

</div>
<div
  className="
    bg-yellow-500/10
    border
    border-yellow-500/20
    rounded-xl
    p-5
    my-8
  "
>

  <p className="text-slate-400 mb-2">
    Advantage
  </p>

  <h3
    className="
      text-yellow-400
      text-2xl
      font-bold
      mb-2
    "
  >
    🏆{" "}
    {winner === "a"
      ? result.player_a.name
      : result.player_b.name}
  </h3>

  <p className="text-slate-300">
    {Math.abs(result.elo_diff)} Elo advantage
  </p>

</div>
<h3
  className="
    text-white
    text-2xl
    font-bold
    mb-6
  "
>
  ⚔ Head-to-Head Details
</h3>
  

  <div className="grid grid-cols-4 gap-4">

    <div
      className="
        bg-slate-950
        rounded-xl
        p-4
        text-center
      "
    >

      <div className="text-slate-400 text-sm">
        Total Games
      </div>

      <div
        className="
          text-blue-400
          text-3xl
          font-bold
        "
      >
        {result.head_to_head.games}
      </div>

    </div>

    <div
      className="
        bg-slate-950
        rounded-xl
        p-4
        text-center
      "
    >

      <div className="text-slate-400 text-sm">
        {result.player_a.name}
      </div>

      <div
        className="
          text-green-400
          text-3xl
          font-bold
        "
      >
        {result.head_to_head.player_a_wins}
      
      </div>

        <div className="text-slate-400 mt-1">
          {Math.round(
            result.head_to_head.player_a_wins /
            result.head_to_head.games *
            100
          )}%
        </div>
    </div>

    <div
      className="
        bg-slate-950
        rounded-xl
        p-4
        text-center
      "
    >

      <div className="text-slate-400 text-sm">
        Draws
      </div>

      <div
        className="
          text-yellow-400
          text-3xl
          font-bold
        "
      >
        {result.head_to_head.draws}
      </div>
      <div className="text-slate-400 mt-1">
        {Math.round(
          result.head_to_head.draws /
          result.head_to_head.games *
          100
        )}%
      </div>

    </div>

    <div
      className="
        bg-slate-950
        rounded-xl
        p-4
        text-center
      "
    >

      <div className="text-slate-400 text-sm">
        {result.player_b.name}
      </div>

      <div
        className="
          text-red-400
          text-3xl
          font-bold
        "
      >
        {result.head_to_head.player_b_wins}
      </div>
      <div className="text-slate-400 mt-1">
        {Math.round(
          result.head_to_head.player_b_wins /
          result.head_to_head.games *
          100
        )}%
      </div>

    </div>

  </div>

</div>

              

             <RatingComparisonChart
              data={ratingChart}
              playerAName={result.player_a.name}
              playerBName={result.player_b.name}
            />

            </div>

          

      )}

    </div>

  );

}

export default Compare;
