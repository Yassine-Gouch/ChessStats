import { useState } from "react";

function Predict() {

  const [whitePlayer, setWhitePlayer] =
    useState("");

  const [blackPlayer, setBlackPlayer] =
    useState("");

  const [selectedWhite, setSelectedWhite] =
    useState(null);

  const [selectedBlack, setSelectedBlack] =
    useState(null);

  const [whiteSuggestions, setWhiteSuggestions] =
    useState([]);

  const [blackSuggestions, setBlackSuggestions] =
    useState([]);

  const [prediction, setPrediction] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  async function searchWhite(value) {

    setWhitePlayer(value);
    setSelectedWhite(null);

    if (value.length < 2) {
      setWhiteSuggestions([]);
      return;
    }

    try {

      const response = await fetch(
        `https://chessstats-jwakvg.fly.dev/players/search?q=${value}`
      );

      const data =
        await response.json();

      setWhiteSuggestions(data);

    } catch (error) {

      console.error(error);

    }
  }

  async function searchBlack(value) {

    setBlackPlayer(value);
    setSelectedBlack(null);

    if (value.length < 2) {

      setBlackSuggestions([]);

      return;
    }

    try {

      const response = await fetch(
        `https://chessstats-jwakvg.fly.dev/players/search?q=${value}`
      );

      const data =
        await response.json();

      setBlackSuggestions(data);

    } catch (error) {

      console.error(error);

    }
  }

  async function handlePredict() {

    if (
      !selectedWhite ||
      !selectedBlack
    ) {

      alert(
        "Select both players from suggestions."
      );

      return;
    }
    if (
      selectedWhite.fideid ===
      selectedBlack.fideid
    ) {

      alert(
        "White and Black players must be different."
      );

      return;
    }
    setLoading(true);

    try {

      const response =
        await fetch(
          "https://chessstats-jwakvg.fly.dev/predict",
          {
            method: "POST",
            headers: {
              "Content-Type":
                "application/json"
            },
            body: JSON.stringify({
              white:
                selectedWhite.name,
              black:
                selectedBlack.name
            })
          }
        );

      const data =
        await response.json();

      setPrediction(data);

    } catch (error) {

      console.error(error);

    }

    setLoading(false);
  }

  return (
    <div className="max-w-7xl">

      {/* HERO */}

      <div className="mb-10">

        <h1
          className="
            text-5xl
            font-bold
            text-white
            mb-4
          "
        >
          🔮 Match Prediction
        </h1>

        <p
          className="
            text-slate-400
            text-xl
          "
        >
          Predict match outcomes using our
          XGBoost model trained on
          471,267 historical games.
        </p>

      </div>

      {/* SEARCH CARD */}

      <div
        className="
          bg-slate-900
          border
          border-slate-800
          rounded-2xl
          p-6
          mb-8
        "
      >

        <div
          className="
            grid
            md:grid-cols-2
            gap-6
          "
        >

          {/* WHITE */}

          <div className="relative">

            <label
              className="
                text-green-400
                font-medium
                block
                mb-2
              "
            >
              White Player
            </label>

            <input
              type="text"
              value={whitePlayer}
              placeholder="Magnus Carlsen..."
              onChange={(e) =>
                searchWhite(
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
                focus:border-green-500
              "
            />

            {whiteSuggestions.length > 0 && (

              <div
                className="
                  absolute
                  mt-2
                  w-full
                  bg-slate-950
                  border
                  border-slate-700
                  rounded-xl
                  overflow-hidden
                  z-50
                "
              >

                {whiteSuggestions.map(
                  (player) => (

                    <div
                      key={
                        player.fideid
                      }
                      onClick={() => {

                        setWhitePlayer(
                          player.name
                        );

                        setSelectedWhite(
                          player
                        );

                        setWhiteSuggestions(
                          []
                        );
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

          </div>

          {/* BLACK */}

          <div className="relative">

            <label
              className="
                text-red-400
                font-medium
                block
                mb-2
              "
            >
              Black Player
            </label>

            <input
              type="text"
              value={blackPlayer}
              placeholder="Fabiano Caruana..."
              onChange={(e) =>
                searchBlack(
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
                focus:border-red-500
              "
            />

            {blackSuggestions.length > 0 && (

              <div
                className="
                  absolute
                  mt-2
                  w-full
                  bg-slate-950
                  border
                  border-slate-700
                  rounded-xl
                  overflow-hidden
                  z-50
                "
              >

                {blackSuggestions.map(
                  (player) => (

                    <div
                      key={
                        player.fideid
                      }
                      onClick={() => {

                        setBlackPlayer(
                          player.name
                        );

                        setSelectedBlack(
                          player
                        );

                        setBlackSuggestions(
                          []
                        );
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

          </div>

        </div>

        <button
          onClick={handlePredict}
          disabled={loading}
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
          {loading
            ? "Analyzing..."
            : "🔮 Predict Match"}
        </button>

      </div>

      {/* RESULT */}

      {prediction && (

        <div
          className="
            space-y-6
          "
        >

          {/* MAIN RESULT */}

          <div
            className="
              bg-slate-900
              border
              border-slate-800
              rounded-2xl
              p-8
              text-center
            "
          >

            <div
              className="
                text-slate-400
                mb-2
              "
            >
              Predicted Result
            </div>

            <div
              className="
                text-5xl
                font-bold
                text-yellow-400
              "
            >
              {prediction.prediction}
            </div>

          </div>

          {/* PROBABILITIES */}

          <div
            className="
              bg-slate-900
              border
              border-slate-800
              rounded-2xl
              p-6
            "
          >

            <h2
              className="
                text-white
                text-2xl
                font-bold
                mb-6
              "
            >
              Winning Chances
            </h2>

            <div className="space-y-5">

              <div>

                <div
                  className="
                    flex
                    justify-between
                    text-white
                    mb-2
                  "
                >
                  <span>
                    {prediction.white}
                  </span>

                  <span>
                    {prediction.white_win}%
                  </span>

                </div>

                <div
                  className="
                    h-3
                    bg-slate-800
                    rounded-full
                  "
                >
                  <div
                    className="
                      h-3
                      rounded-full
                      bg-green-500
                    "
                    style={{
                      width:
                        `${prediction.white_win}%`
                    }}
                  />
                </div>

              </div>

              <div>

                <div
                  className="
                    flex
                    justify-between
                    text-white
                    mb-2
                  "
                >
                  <span>Draw</span>

                  <span>
                    {prediction.draw}%
                  </span>

                </div>

                <div
                  className="
                    h-3
                    bg-slate-800
                    rounded-full
                  "
                >
                  <div
                    className="
                      h-3
                      rounded-full
                      bg-yellow-500
                    "
                    style={{
                      width:
                        `${prediction.draw}%`
                    }}
                  />
                </div>

              </div>

              <div>

                <div
                  className="
                    flex
                    justify-between
                    text-white
                    mb-2
                  "
                >
                  <span>
                    {prediction.black}
                  </span>

                  <span>
                    {prediction.black_win}%
                  </span>

                </div>

                <div
                  className="
                    h-3
                    bg-slate-800
                    rounded-full
                  "
                >
                  <div
                    className="
                      h-3
                      rounded-full
                      bg-red-500
                    "
                    style={{
                      width:
                        `${prediction.black_win}%`
                    }}
                  />
                </div>

              </div>

            </div>

          </div>

          {/* INSIGHTS */}

          <div
            className="
              grid
              md:grid-cols-4
              gap-4
            "
          >

            <div
              className="
                bg-slate-900
                rounded-2xl
                p-5
              "
            >
              <p className="text-slate-400">
                White Rating
              </p>

              <h3
                className="
                  text-white
                  text-3xl
                  font-bold
                "
              >
                {prediction.white_rating}
              </h3>
            </div>

            <div
              className="
                bg-slate-900
                rounded-2xl
                p-5
              "
            >
              <p className="text-slate-400">
                Black Rating
              </p>

              <h3
                className="
                  text-white
                  text-3xl
                  font-bold
                "
              >
                {prediction.black_rating}
              </h3>
            </div>

            <div
              className="
                bg-slate-900
                rounded-2xl
                p-5
              "
            >
              <p className="text-slate-400">
                Elo Difference
              </p>

              <h3
                className="
                  text-blue-400
                  text-3xl
                  font-bold
                "
              >
                {prediction.white_rating -
                  prediction.black_rating}
              </h3>
            </div>

            <div
              className="
                bg-slate-900
                rounded-2xl
                p-5
              "
            >
              <p className="text-slate-400">
                Head‑to‑Head
              </p>

              <h3
                className="
                  text-yellow-400
                  text-3xl
                  font-bold
                "
              >
                {prediction.h2h_games}
              </h3>
            </div>

          </div>

          {/* MODEL */}

          <div
            className="
              bg-slate-900
              border
              border-slate-800
              rounded-2xl
              p-6
            "
          >
            <h3
              className="
                text-white
                text-xl
                font-bold
                mb-4
              "
            >
              Model Information
            </h3>

            <div
              className="
                grid
                md:grid-cols-4
                gap-4
                text-slate-300
              "
            >
              <div>XGBoost</div>
              <div>471,267 Games</div>
              <div>31 Features</div>
              <div>61.67% Accuracy</div>
            </div>

          </div>

        </div>

      )}

    </div>
  );
}

export default Predict;
