import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

function RatingChart({ data }) {

  if (!data || data.length === 0) {

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
          📈 Rating History
        </h2>

        <p className="text-slate-400">
          No rating history found.
        </p>

      </div>

    );

  }

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
          mb-6
        "
      >
        📈 Rating History
      </h2>

      <LineChart
        width={1000}
        height={400}
        data={data}
        margin={{
          top: 20,
          right: 20,
          left: 10,
          bottom: 10
        }}
      >

        <CartesianGrid
          stroke="#1e293b"
          strokeDasharray="3 3"
        />

        <XAxis
          dataKey="date"
          tick={{ fill: "#94a3b8" }}
          stroke="#475569"
          minTickGap={50}
        />

        <YAxis
          stroke="#475569"
          tick={{ fill: "#94a3b8" }}
          domain={[
            "dataMin - 20",
            "dataMax + 20"
          ]}
        />

        <Tooltip
          contentStyle={{
            backgroundColor: "#0f172a",
            border: "1px solid #334155",
            borderRadius: "12px",
            color: "#ffffff"
          }}
        />

        <Line
          type="monotone"
          dataKey="rating"
          stroke="#3b82f6"
          strokeWidth={4}
          dot={false}
          animationDuration={1500}
          activeDot={{
            r: 6,
            fill: "#60a5fa"
          }}
        />

      </LineChart>

    </div>

  );

}

export default RatingChart;