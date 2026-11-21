import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import RatingChart from "../components/RatingChart";


import OpeningsCard from "../components/OpeningsCard";

import {
  getPlayerRatingHistory,
  getPlayerOpenings
} from "../services/api";

function PlayerProfile() {

  const { name } = useParams();

  const [player, setPlayer] = useState(null);

  const [history, setHistory] = useState([]);

  const [loading, setLoading] = useState(true);
  const [openings, setOpenings] =
  useState([]);

  useEffect(() => {

    async function loadPlayer() {

      try {

        const response = await fetch(
          `http://127.0.0.1:8000/players/profile/${name}`
        );

        const playerData =
          await response.json();

        setPlayer(playerData);

        const historyData =
          await getPlayerRatingHistory(
            name
          );

        setHistory(historyData);
        const openingsData =
         await getPlayerOpenings(
            name
          );

        setOpenings(
           openingsData
        );

      } catch (error) {

        console.error(error);

      }

      setLoading(false);

    }

    loadPlayer();

  }, [name]);

  if (loading) {

    return (

      <div className="text-white text-xl">
        Loading...
      </div>

    );

  }

  if (!player) {

    return (

      <div className="text-red-400 text-xl">
        Player not found
      </div>

    );

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
          ♟ Player Profile
        </span>

        <h1
          className="
            text-5xl
            font-bold
            text-white
            mb-4
          "
        >
          {player.name}
        </h1>

        <p
          className="
            text-xl
            text-slate-400
          "
        >
          {player.title || "Player"} • {player.country}
        </p>

      </div>

      {/* STATS */}

      <div className="grid grid-cols-2 gap-6 mb-10">

        <div
          className="
            bg-slate-900
            border
            border-slate-800
            rounded-2xl
            p-6
          "
        >
          <p className="text-slate-400 mb-2">
            ⭐ Rating
          </p>

          <h2
            className="
              text-4xl
              font-bold
              text-white
            "
          >
            {player.rating}
          </h2>

        </div>

        <div
          className="
            bg-slate-900
            border
            border-slate-800
            rounded-2xl
            p-6
          "
        >
          <p className="text-slate-400 mb-2">
            🎮 Games
          </p>

          <h2
            className="
              text-4xl
              font-bold
              text-white
            "
          >
            {player.games}
          </h2>

        </div>

        <div
          className="
            bg-slate-900
            border
            border-slate-800
            rounded-2xl
            p-6
          "
        >
          <p className="text-slate-400 mb-2">
            📈 Last Elo
          </p>

          <h2
            className="
              text-4xl
              font-bold
              text-white
            "
          >
            {player.last_elo}
          </h2>

        </div>

        <div
          className="
            bg-slate-900
            border
            border-slate-800
            rounded-2xl
            p-6
          "
        >
          <p className="text-slate-400 mb-2">
            🆔 FIDE ID
          </p>

          <h2
            className="
              text-2xl
              font-bold
              text-white
            "
          >
            {player.fideid}
          </h2>

        </div>

      </div>

      {/* RATING CHART */}

      <div className="mt-10">

      <RatingChart
       data={history}
      />

      </div>
      <div className="mt-10">

        <OpeningsCard
            openings={openings}
        />

       </div>

    </div>

  );

}

export default PlayerProfile;