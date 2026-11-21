import { useEffect, useState } from "react";

import { getInfo } from "../services/api";

import StatCard from "../components/StatCard";

function Dashboard() {

  const [info, setInfo] = useState(null);

  useEffect(() => {

    async function load() {

      const data = await getInfo();

      setInfo(data);

    }

    load();

  }, []);

  if (!info) {

    return (

      <div className="text-white text-xl">

        Loading...

      </div>

    );

  }

  return (

    <div className="max-w-7xl">

      {/* HERO */}

      <div className="mb-14">

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
          ♟ Professional Chess Intelligence
        </span>

        <h1
          className="
            text-5xl
            xl:text-6xl
            font-bold
            text-white
            leading-tight
            mb-6
            max-w-4xl
          "
        >
          Professional Chess
          <br />
          Analytics Platform
        </h1>

        <p
          className="
            text-slate-400
            text-xl
            max-w-4xl
            mb-8
          "
        >
          Predict outcomes, compare players,
          analyze openings and explore tournament
          performance using machine learning and
          advanced chess analytics.
        </p>

        <div className="flex gap-4">

          <button
            className="
              px-6
              py-3
              rounded-xl
              bg-blue-600
              hover:bg-blue-700
              font-semibold
              text-white
              transition
            "
          >
            Start Predicting
          </button>

          <button
            className="
              px-6
              py-3
              rounded-xl
              border
              border-slate-700
              hover:border-slate-500
              text-white
              transition
            "
          >
            Explore Players
          </button>

        </div>

      </div>

      {/* KPI CARDS */}

      <div className="grid grid-cols-2 gap-6 mb-20">

        <StatCard
          title="🎮 Games"
          value={info.games.toLocaleString()}
        />

        <StatCard
          title="👥 Players"
          value={info.players.toLocaleString()}
        />

        <StatCard
          title="🎯 Accuracy"
          value={`${info.accuracy}%`}
        />

        <StatCard
          title="🤖 Model"
          value={info.model}
        />

      </div>

      {/* HIGHLIGHTS */}

      <div>

        <h2
          className="
            text-2xl
            font-bold
            text-white
            mb-6
          "
        >
          Recent Highlights
        </h2>

        <div className="grid grid-cols-3 gap-6">

          <div
            className="
              bg-slate-900
              border
              border-slate-800
              rounded-2xl
              p-6
            "
          >
            <p className="text-blue-400 mb-3">
              🏆 Most Popular Player
            </p>

            <h3 className="text-white text-xl font-semibold">
              Magnus Carlsen
            </h3>

            <p className="text-slate-400 mt-2">
              Highest search volume
            </p>
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
            <p className="text-green-400 mb-3">
              🔥 Best Model
            </p>

            <h3 className="text-white text-xl font-semibold">
              XGBoost
            </h3>

            <p className="text-slate-400 mt-2">
              Accuracy {info.accuracy}%
            </p>
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
            <p className="text-purple-400 mb-3">
              ♟ Dataset
            </p>

            <h3 className="text-white text-xl font-semibold">
              {info.games.toLocaleString()}
            </h3>

            <p className="text-slate-400 mt-2">
              Professional Chess Games
            </p>
          </div>

        </div>

      </div>

    </div>

  );

}

export default Dashboard;