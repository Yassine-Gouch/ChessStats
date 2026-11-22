import { OPENING_NAMES } from "../data/openingNames";

function OpeningsCard({ openings }) {

  if (!openings || openings.length === 0) {

    return (

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
            mb-4
          "
        >
          ♟ Favorite Openings
        </h2>

        <p className="text-slate-400">
          No openings found.
        </p>

      </div>

    );

  }

  const maxGames = openings[0].games;

  return (

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
          mb-8
        "
      >
        ♟ Favorite Openings
      </h2>

      <div className="space-y-6">

        {openings.map((opening, index) => {

          const openingName =
            OPENING_NAMES[opening.eco] ||
            opening.eco;

          const progress =
            (opening.games / maxGames) * 100;

          let medal = `#${index + 1}`;

          if (index === 0) medal = "🥇";
          if (index === 1) medal = "🥈";
          if (index === 2) medal = "🥉";

          return (

            <div key={opening.eco}>

              <div className="flex justify-between items-start mb-2">

                <div>

                  <div
                    className="
                      text-white
                      font-semibold
                      text-lg
                    "
                  >
                    {medal} {openingName}
                  </div>

                  <div
                    className="
                      text-slate-400
                      text-sm
                    "
                  >
                    ECO: {opening.eco}
                  </div>

                </div>

                <div
                  className="
                    text-blue-400
                    font-bold
                  "
                >
                  {opening.games} games
                </div>

              </div>

              <div
                className="
                  w-full
                  h-3
                  bg-slate-800
                  rounded-full
                  overflow-hidden
                "
              >

                <div
                  className="
                    h-full
                    bg-blue-500
                    rounded-full
                    transition-all
                    duration-700
                  "
                  style={{
                    width: `${progress}%`
                  }}
                />

              </div>

            </div>

          );

        })}

      </div>

    </div>

  );

}

export default OpeningsCard;
