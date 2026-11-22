function StatCard({ title, value }) {

  return (

    <div
      className="
        bg-slate-900
        border
        border-slate-800
        rounded-2xl
        p-6
        hover:border-blue-600
        hover:shadow-lg
        hover:shadow-blue-500/10
        transition-all
        duration-300
      "
    >

      <p
        className="
          text-slate-400
          text-sm
          mb-3
        "
      >
        {title}
      </p>

      <h2
        className="
          text-4xl
          font-bold
          text-white
        "
      >
        {value}
      </h2>

    </div>

  );

}

export default StatCard;
