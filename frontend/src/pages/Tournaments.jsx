import { useEffect, useState } from "react";

import {
  getTournamentsStats,
  getTopTournaments,
  getTournamentDetails
} from "../services/api";

function Tournaments() {

  const [stats, setStats] =
    useState(null);

  const [tournaments, setTournaments] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [search, setSearch] =
    useState("");

  const [expandedTournament, setExpandedTournament] =
    useState(null);

  const [selectedTournament, setSelectedTournament] =
    useState(null);

  useEffect(() => {

    async function loadData() {

      try {

        const statsData =
          await getTournamentsStats();

        const tournamentsData =
          await getTopTournaments();

        setStats(statsData);

        setTournaments(
          tournamentsData
        );

      } catch (error) {

        console.error(error);

      }

      setLoading(false);
    }

    loadData();

  }, []);

  async function handleTournamentClick(
    event,
    year
  ) {

    const key =
      `${event}-${year}`;

    if (
      expandedTournament === key
    ) {

      setExpandedTournament(
        null
      );

      setSelectedTournament(
        null
      );

      return;
    }

    try {

      const data =
        await getTournamentDetails(
          event,
          year
        );

      setSelectedTournament(
        data
      );

      setExpandedTournament(
        key
      );

    } catch (error) {

      console.error(error);
    }
  }

  const filteredTournaments =
    tournaments.filter(
      (tournament) =>
        tournament.event
          .toLowerCase()
          .includes(
            search.toLowerCase()
          )
    );

  if (loading) {

    return (
      <div className="text-slate-400">
        Loading tournaments...
      </div>
    );
  }

  return (

    <div className="space-y-8">

      <div>

        <h1 className="text-5xl font-bold text-white mb-4">
          🏆 Tournament Explorer
        </h1>

        <p className="text-slate-400 text-xl">
          Explore chess tournaments,
          strength, participation and
          performance.
        </p>

      </div>

      {stats && (

        <div className="grid md:grid-cols-4 gap-4">

          <div className="bg-slate-900 rounded-2xl p-5">

            <p className="text-slate-400">
              Total Tournaments
            </p>

            <h3 className="text-white text-3xl font-bold">
              {stats.total_tournaments}
            </h3>

          </div>

          <div className="bg-slate-900 rounded-2xl p-5">

            <p className="text-slate-400">
              Most Played
            </p>

            <h3 className="text-white font-bold">
              {stats.most_played.event}
            </h3>

            <p className="text-slate-500">
              {
                stats.most_played.games
              } games
            </p>

          </div>

          <div className="bg-slate-900 rounded-2xl p-5">

            <p className="text-slate-400">
              Strongest Tournament
            </p>

            <h3 className="text-white font-bold">
              {stats.strongest.event}
            </h3>

            <p className="text-amber-400">
              {stats.strongest.avg_elo}
            </p>

          </div>

          <div className="bg-slate-900 rounded-2xl p-5">

            <p className="text-slate-400">
              Average Elo
            </p>

            <h3 className="text-white text-3xl font-bold">
              {stats.average_elo}
            </h3>

          </div>

        </div>

      )}

      <div className="bg-slate-900 rounded-2xl p-6">

        <input
          type="text"
          placeholder="Search tournament..."
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
          "
        />

      </div>

      <div className="bg-slate-900 rounded-2xl overflow-hidden">

        <div className="overflow-x-auto">

          <table className="w-full">

            <thead className="bg-slate-950">

              <tr>

                <th className="p-4 text-left">
                  Tournament
                </th>

                <th className="p-4 text-left">
                  Year
                </th>

                <th className="p-4 text-left">
                  Games
                </th>

                <th className="p-4 text-left">
                  Players
                </th>

                <th className="p-4 text-left">
                  Avg Elo
                </th>

              </tr>

            </thead>

            <tbody>

              {filteredTournaments.map(
                (
                  tournament
                ) => (

                  <>

                    <tr
                      onClick={() =>
                        handleTournamentClick(
                          tournament.event,
                          tournament.year
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
                        {tournament.event}
                      </td>

                      <td className="p-4 text-slate-300">
                        {tournament.year}
                      </td>

                      <td className="p-4 text-slate-300">
                        {tournament.games_count}
                      </td>

                      <td className="p-4 text-slate-300">
                        {tournament.players_count}
                      </td>

                      <td className="p-4 text-amber-400">
                        {tournament.avg_elo}
                      </td>

                    </tr>

                    {
                      expandedTournament ===
                      `${tournament.event}-${tournament.year}`
                      &&
                      selectedTournament && (

                        <tr>

                          <td
                            colSpan="5"
                            className="bg-slate-950 p-6"
                          >

                            <div className="grid md:grid-cols-3 gap-4 mb-6">

                              <div className="bg-slate-900 rounded-xl p-4">

                                <p className="text-slate-400">
                                  Games
                                </p>

                                <h3 className="text-white text-3xl font-bold">
                                  {
                                    selectedTournament.games_count
                                  }
                                </h3>

                              </div>

                              <div className="bg-slate-900 rounded-xl p-4">

                                <p className="text-slate-400">
                                  Players
                                </p>

                                <h3 className="text-white text-3xl font-bold">
                                  {
                                    selectedTournament.players_count
                                  }
                                </h3>

                              </div>

                              <div className="bg-slate-900 rounded-xl p-4">

                                <p className="text-slate-400">
                                  Avg Elo
                                </p>

                                <h3 className="text-amber-400 text-3xl font-bold">
                                  {
                                    selectedTournament.avg_elo
                                  }
                                </h3>

                              </div>

                            </div>

                            <div className="grid md:grid-cols-3 gap-4 mb-6">

                              <div className="bg-slate-900 rounded-xl p-4">

                                <p className="text-slate-400">
                                  Location
                                </p>

                                <h3 className="text-white font-bold">
                                  {
                                    selectedTournament.site
                                  }
                                </h3>

                              </div>

                              <div className="bg-slate-900 rounded-xl p-4">

                                <p className="text-slate-400">
                                  Duration
                                </p>

                                <h3 className="text-white font-bold">
                                  {
                                    selectedTournament.duration_days
                                  }
                                  {" "}
                                  days
                                </h3>

                              </div>

                              <div className="bg-slate-900 rounded-xl p-4">

                                <p className="text-slate-400">
                                  Strength
                                </p>

                                <h3 className="text-green-400 font-bold">
                                  {
                                    selectedTournament.strength
                                  }
                                </h3>

                              </div>

                            </div>

                            <div className="space-y-5">

                              <div>

                                <div className="flex justify-between mb-2">

                                  <span className="text-yellow-400">
                                    Draw Rate
                                  </span>

                                  <span className="text-white">
                                    {
                                      selectedTournament.draw_rate
                                    }%
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
                                      `${selectedTournament.draw_rate}%`
                                    }}
                                  />

                                </div>

                              </div>

                              <div>

                                <div className="flex justify-between mb-2">

                                  <span className="text-green-400">
                                    Decisive Rate
                                  </span>

                                  <span className="text-white">
                                    {
                                      selectedTournament.decisive_rate
                                    }%
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
                                      `${selectedTournament.decisive_rate}%`
                                    }}
                                  />

                                </div>

                              </div>

                            </div>

                          </td>

                        </tr>

                      )
                    }

                  </>

                )
              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>

  );
}

export default Tournaments;