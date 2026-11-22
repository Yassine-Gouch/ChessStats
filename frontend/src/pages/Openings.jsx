import React, {
  useEffect,
  useState
} from "react";

import {
  getOpeningName
} from "../data/openingNames";

function Openings() {

  const [stats, setStats] =
    useState(null);

  const [openings, setOpenings] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [search, setSearch] =
    useState("");

  const [selectedOpening, setSelectedOpening] =
    useState(null);

  const [expandedEco, setExpandedEco] =
  useState(null);

  

  const [topPlayer, setTopPlayer] =
  useState(null);
  useEffect(() => {

    async function loadData() {

      try {

        const statsResponse =
          await fetch(
            "https://chessstats-jwakvg.fly.dev/openings/stats"
          );

        const statsData =
          await statsResponse.json();

        setStats(statsData);

        const openingsResponse =
          await fetch(
            "https://chessstats-jwakvg.fly.dev/openings/top"
          );

        const openingsData =
          await openingsResponse.json();

        setOpenings(openingsData);

      } catch (error) {

        console.error(error);

      }

      setLoading(false);
    }

    loadData();

  }, []);

  async function handleOpeningClick(
  eco
) {

  console.log(
    "clicked",
    eco
  );
  if (expandedEco === eco) {

  setExpandedEco(null);

  setSelectedOpening(null);

  return;
}

  try {

    const response =
      await fetch(
        `https://chessstats-jwakvg.fly.dev/openings/${eco}`
      );

    const data =
      await response.json();

    console.log(data);
    const playerResponse =
      await fetch(
        `https://chessstats-jwakvg.fly.dev/openings/${eco}/top-player`
      );

    const playerData =
      await playerResponse.json();

    setTopPlayer(
      playerData
    );
    setSelectedOpening(data);
    setExpandedEco(eco);

  } catch (error) {

    console.error(error);

  }
}

  const filteredOpenings =
    openings.filter(
      (opening) => {

        const openingName =
          getOpeningName(
            opening.eco
          );

        const query =
          search.toLowerCase();

        return (
          opening.eco
            .toLowerCase()
            .includes(query)
          ||
          openingName
            .toLowerCase()
            .includes(query)
        );
      }
    );

  if (loading) {

    return (
      <div className="text-slate-400">
        Loading openings...
      </div>
    );
  }

  return (

    <div className="space-y-8">

      {/* HERO */}

      <div>

        <h1
          className="
            text-5xl
            font-bold
            text-white
            mb-4
          "
        >
          ♟ Openings Explorer
        </h1>

        <p
          className="
            text-slate-400
            text-xl
          "
        >
          Explore opening popularity,
          performance and results from
          hundreds of thousands of games.
        </p>

      </div>

      {/* STATS */}

      {stats && (

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
              Total Openings
            </p>

            <h3
              className="
                text-white
                text-3xl
                font-bold
              "
            >
              {stats.total_openings}
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
              Most Played
            </p>

            <h3
              className="
                text-white
                font-bold
              "
            >
              {
                getOpeningName(
                  stats.most_played.eco
                )
              }
            </h3>

            <p className="text-slate-500">
              {
                stats.most_played.games
              } games
            </p>

          </div>

          <div
            className="
              bg-slate-900
              rounded-2xl
              p-5
            "
          >
            <p className="text-slate-400">
              Best For White
            </p>

            <h3
              className="
                text-white
                font-bold
              "
            >
              {
                getOpeningName(
                  stats.white_best.eco
                )
              }
            </h3>

            <p className="text-green-400">
              {
                stats.white_best.win_rate
              }%
            </p>

          </div>

          <div
            className="
              bg-slate-900
              rounded-2xl
              p-5
            "
          >
            <p className="text-slate-400">
              Highest Draw Rate
            </p>

            <h3
              className="
                text-white
                font-bold
              "
            >
              {
                getOpeningName(
                  stats.highest_draw.eco
                )
              }
            </h3>

            <p className="text-yellow-400">
              {
                stats.highest_draw.draw_rate
              }%
            </p>

          </div>

        </div>

      )}

      {/* SEARCH */}

      <div
        className="
          bg-slate-900
          rounded-2xl
          p-6
        "
      >

        <input
          type="text"
          placeholder="
            Search opening...
          "
          value={search}
          onChange={(e) =>
            setSearch(
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
          "
        />

      </div>

      {/* TABLE */}

      <div
        className="
          bg-slate-900
          rounded-2xl
          overflow-hidden
        "
      >

        <div
          className="
            overflow-x-auto
          "
        >

          <table
            className="
              w-full
            "
          >

            <thead
              className="
                bg-slate-950
              "
            >

              <tr>

                <th className="p-4 text-left text-slate-300">
                  ECO
                </th>

                <th className="p-4 text-left text-slate-300">
                  Opening
                </th>

                <th className="p-4 text-left text-slate-300">
                  Games
                </th>

                <th className="p-4 text-left text-green-400">
                  White
                </th>

                <th className="p-4 text-left text-yellow-400">
                  Draw
                </th>

                <th className="p-4 text-left text-red-400">
                  Black
                </th>

              </tr>

            </thead>

            <tbody>

              {filteredOpenings.map(
                (opening) => (

                  <React.Fragment
                      key={opening.eco}
                    >


                    <tr
                      onClick={() =>
                        handleOpeningClick(
                          opening.eco
                        )
                      }
                      className="
                        border-t
                        border-slate-800
                        cursor-pointer
                        hover:bg-slate-800
                      "
                    >

                      <td className="p-4 text-white">
                        {opening.eco}
                      </td>

                      <td className="p-4 text-slate-300">
                        {
                          getOpeningName(
                            opening.eco
                          )
                        }
                      </td>

                      <td className="p-4 text-slate-300">
                        {opening.games}
                      </td>

                      <td className="p-4 text-green-400">
                        {opening.white_win_rate}%
                      </td>

                      <td className="p-4 text-yellow-400">
                        {opening.draw_rate}%
                      </td>

                      <td className="p-4 text-red-400">
                        {opening.black_win_rate}%
                      </td>

                    </tr>

                    {
                     expandedEco === opening.eco &&
                    selectedOpening?.eco === opening.eco && (

                        <tr>

                          <td
                            colSpan="6"
                            className="
                              bg-slate-950
                              text-center
                              p-4
                            "
                          >

                          <div
                            className="
                              bg-slate-900
                              rounded-xl
                              p-6
                            "
                          >


      {/* DETAILS */}

      {selectedOpening && (

        <div
          className="
            bg-slate-900
            rounded-2xl
            p-6
          "
        >

          

          <div
            className="
              grid
              md:grid-cols-3
              gap-4
            "
          >

            <div
              className="
                bg-slate-950
                rounded-xl
                p-4
              "
            >
              <p className="text-slate-400">
                Games
              </p>

              <h3
                className="
                  text-white
                  text-3xl
                  font-bold
                "
              >
                {selectedOpening.games}
              </h3>
            </div>

           
          <div
            className="
              bg-slate-950
              rounded-xl
              p-4
            "
          >

            <p className="text-slate-400">
              Average Elo
             </p>

            <h3
              className="
                text-white
                text-3xl
                font-bold
              "
            >
              {
                Math.round(
                  (
                    selectedOpening.avg_white_elo +
                    selectedOpening.avg_black_elo
                  ) / 2
                )
              }
            </h3>

          </div>

          <div
            className="
              bg-slate-950
              rounded-xl
              p-4
            "
          >

            <p className="text-slate-400">
              White Advantage
            </p>

            <h3
             className={`
                text-3xl
                font-bold
                ${
                  (
                    selectedOpening.white_win_rate -
                    selectedOpening.black_win_rate
                  ) >= 0
                    ? "text-green-400"
                    : "text-red-400"
                }
              `}
            >
              {(
                selectedOpening.white_win_rate -
                selectedOpening.black_win_rate
              ).toFixed(2)}
              %
            </h3>

          </div>

          </div>
          {topPlayer && (

            <div
              className="
                mt-6
                bg-slate-950
                rounded-xl
                p-4
                text-center
              "
            >

              <p className="text-slate-400">
                Top Expert
              </p>

              <h3
                className="
                  text-white
                  text-2xl
                  font-bold
                "
              >
                {topPlayer.name}
              </h3>

              <div
                className="
                  flex
                  justify-center
                  gap-12
                  mt-4
                "
              >

                  <div className="text-center">
                  <p className="text-slate-500 text-sm">
                    Peak Elo
                  </p>

                  <p className="text-amber-400 font-bold">
                    {topPlayer.rating}
                  </p>
                </div>

                    <div className="text-center">
                    <p className="text-slate-500 text-sm">
                    Games
                  </p>

                  <p className="text-white font-bold">
                    {topPlayer.games}
                  </p>
                </div>

              </div>

            </div>

          )}
         <div className="mt-6 space-y-5">

  <div>

    <div className="flex justify-between mb-2">

      <span className="text-green-400">
        White Wins
      </span>

      <span className="text-white">
        {selectedOpening.white_win_rate}%
      </span>

    </div>

    <div className="bg-slate-800 h-3 rounded-full">

      <div
        className="
          bg-green-500
          h-3
          rounded-full
        "
        style={{
          width:
          `${selectedOpening.white_win_rate}%`
        }}
      />

    </div>

  </div>

  <div>

    <div className="flex justify-between mb-2">

      <span className="text-yellow-400">
        Draws
      </span>

      <span className="text-white">
        {selectedOpening.draw_rate}%
      </span>

    </div>

    <div className="bg-slate-800 h-3 rounded-full">

      <div
        className="
          bg-yellow-500
          h-3
          rounded-full
        "
        style={{
          width:
          `${selectedOpening.draw_rate}%`
        }}
      />

    </div>

  </div>

  <div>

    <div className="flex justify-between mb-2">

      <span className="text-red-400">
        Black Wins
      </span>

      <span className="text-white">
        {selectedOpening.black_win_rate}%
      </span>

    </div>

    <div className="bg-slate-800 h-3 rounded-full">

      <div
        className="
          bg-red-500
          h-3
          rounded-full
        "
        style={{
          width:
          `${selectedOpening.black_win_rate}%`
        }}
      />

    </div>

  </div>

</div> 

        </div>

      )}

                          </div>

                          </td>

                        </tr>

                      )
                    }

                  </React.Fragment>

                )
              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}

export default Openings;
