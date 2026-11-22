import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";



function RatingComparisonChart({
  data,
  playerAName,
  playerBName
}) {

    const minRating = Math.min(
  ...data.flatMap(d => [
    d.playerA ?? Infinity,
    d.playerB ?? Infinity
  ])
);

const maxRating = Math.max(
  ...data.flatMap(d => [
    d.playerA ?? -Infinity,
    d.playerB ?? -Infinity
  ])
);

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
        📈 Rating History VS
      </h2>

      <ResponsiveContainer
        width="100%"
        height={400}
      >

        <LineChart data={data}>

          <XAxis dataKey="date" />
          

          <YAxis
            domain={[
                minRating - 20,
                maxRating + 20
            ]}
            />

          <Tooltip />

          <Legend />

          <Line
            dataKey="playerA"
            stroke="#3b82f6"
            strokeWidth={3}
            dot={false}
            name={playerAName}
            />

            <Line
            dataKey="playerB"
            stroke="#22c55e"
            strokeWidth={3}
            dot={false}
            name={playerBName}
            />

        </LineChart>

      </ResponsiveContainer>

    </div>

  );

}

export default RatingComparisonChart;
