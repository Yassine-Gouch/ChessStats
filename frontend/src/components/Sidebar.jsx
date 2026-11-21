import { Link, useLocation } from "react-router-dom";

function Sidebar() {

  const location = useLocation();

  const menuItems = [
    {
      name: "Dashboard",
      path: "/",
      icon: "🏠"
    },
    {
      name: "Players",
      path: "/players",
      icon: "👤"
    },
    {
      name: "Compare",
      path: "/compare",
      icon: "⚔️"
    },
    {
      name: "Predict",
      path: "/predict",
      icon: "🤖"
    },
    {
      name: "Openings",
      path: "/openings",
      icon: "♟️"
    },
    {
      name: "Tournaments",
      path: "/tournaments",
      icon: "🏆"
    }
  ];

  return (

    <aside
      className="
        w-72
        min-h-screen
        bg-slate-900
        border-r
        border-slate-800
        flex
        flex-col
      "
    >

      {/* HEADER */}

      <div
        className="
          p-6
          border-b
          border-slate-800
        "
      >

        <h1
          className="
            text-4xl
            font-bold
            text-white
            mb-3
          "
        >
          ♟ ChessStats
        </h1>

        <p
          className="
            text-slate-400
            text-sm
          "
        >
          Professional Chess Intelligence
        </p>

      </div>

      {/* MENU */}

      <nav className="p-4 flex-1">

        {menuItems.map((item) => (

          <Link
            key={item.path}
            to={item.path}
            className={`
              flex
              items-center
              gap-3
              px-4
              py-3
              rounded-2xl
              mb-2
              transition-all
              duration-300

              ${
                location.pathname === item.path
                  ? "bg-blue-600 text-white shadow-lg shadow-blue-900/30"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
              }
            `}
          >

            <span>{item.icon}</span>

            <span>
              {item.name}
            </span>

          </Link>

        ))}

      </nav>

      {/* SYSTEM STATUS */}

      <div className="p-4">

        <div
          className="
            bg-slate-800
            border
            border-slate-700
            rounded-2xl
            p-4
          "
        >

          <h3
            className="
              text-white
              font-semibold
              mb-4
            "
          >
            🟢 System Status
          </h3>

          <div className="space-y-3">

            <div>

              <p className="text-slate-400 text-sm">
                API
              </p>

              <p className="text-green-400 font-medium">
                Online
              </p>

            </div>

            <div>

              <p className="text-slate-400 text-sm">
                Model
              </p>

              <p className="text-white font-medium">
                XGBoost
              </p>

            </div>

            <div>

              <p className="text-slate-400 text-sm">
                Accuracy
              </p>

              <p className="text-blue-400 font-medium">
                61.67%
              </p>

            </div>

          </div>

        </div>

      </div>

    </aside>

  );

}

export default Sidebar;