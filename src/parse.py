from pathlib import Path
import hashlib

import chess.pgn
import duckdb
import pandas as pd

from src.config import DB_PATH, PROCESSED, RESULT_MAP

def safe_date(date_str):

    if pd.isna(date_str):
        return pd.NaT, True

    date_str = str(date_str).strip()

    if date_str == "":
        return pd.NaT, True

    approx = "??" in date_str

    cleaned = (
        date_str
        .replace("????", "1900")
        .replace("??", "01")
    )

    try:

        date = pd.to_datetime(
            cleaned,
            format="%Y.%m.%d",
            errors="coerce"
        )

    except Exception:

        date = pd.NaT

    return date, approx

def make_game_id(
    event: str,
    date: str,
    round_: str,
    white: str,
    black: str
) -> str:
    """
    Stable unique id for a game.
    """

    text = (
        f"{event}|{date}|{round_}|"
        f"{white}|{black}"
    )

    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()


def games_from_pgn(path: Path):
    """
    Read PGN headers only.
    Fast even on large files.
    """

    with open(
        path,
        encoding="utf-8",
        errors="replace"
    ) as f:

        while True:

            h = chess.pgn.read_headers(f)

            if h is None:
                break

            yield {

                "event": h.get("Event"),
                "site": h.get("Site"),
                "date_raw": h.get("Date"),
                "round": h.get("Round"),

                "white": h.get("White"),
                "black": h.get("Black"),

                "white_elo": h.get("WhiteElo"),
                "black_elo": h.get("BlackElo"),

                "white_fide_id":
                    h.get("WhiteFideId"),

                "black_fide_id":
                    h.get("BlackFideId"),

                "white_title":
                    h.get("WhiteTitle"),

                "black_title":
                    h.get("BlackTitle"),

                "event_date":
                    h.get("EventDate"),

                "ply_count":
                    h.get("PlyCount"),

                "result":
                    h.get("Result"),

                "eco":
                    h.get("ECO")
            }


def main():

    rows = []

    twic_dir = Path("data/raw/twic")

    files = sorted(
        twic_dir.glob("*.pgn")
    )

    print(
        f"Reading {len(files)} PGN files..."
    )

    for pgn in files:

        print(
            f"Reading {pgn.name}"
        )

        rows.extend(
            games_from_pgn(pgn)
        )

    df = pd.DataFrame(rows)

    print(
        f"\nRaw games: {len(df):,}"
    )

    # ---------------------------
    # DATE PARSING
    # ---------------------------

    parsed_dates = (
        df["date_raw"]
        .apply(safe_date)
    )

    df["date"] = parsed_dates.apply(
        lambda x: x[0]
    )

    df["date_approx"] = parsed_dates.apply(
        lambda x: x[1]
    )

    # ---------------------------
    # NUMERIC ELO
    # ---------------------------

    for col in [
        "white_elo",
        "black_elo"
    ]:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # ---------------------------
    # VALID RESULTS ONLY
    # ---------------------------

    df = df[
        df["result"].isin(
            RESULT_MAP.keys()
        )
    ]

    # ---------------------------
    # RESULT SCORE
    # ---------------------------

    df["result_score"] = (
        df["result"]
        .map(RESULT_MAP)
        .astype("int8")
    )

    # ---------------------------
    # GAME ID
    # ---------------------------

    df["game_id"] = df.apply(
        lambda row: make_game_id(
            row["event"],
            row["date_raw"],
            row["round"],
            row["white"],
            row["black"]
        ),
        axis=1
    )

    before = len(df)

    df = df.drop_duplicates(
        subset="game_id"
    )

    duplicates_removed = (
        before - len(df)
    )

    # ---------------------------
    # SAVE PARQUET
    # ---------------------------

    output = (
        PROCESSED /
        "games.parquet"
    )

    df.to_parquet(
        output,
        index=False
    )

    # ---------------------------
    # DUCKDB
    # ---------------------------

    con = duckdb.connect(DB_PATH)

    con.execute("""
        CREATE OR REPLACE TABLE games
        AS
        SELECT *
        FROM 'data/processed/games.parquet'
    """)

    # ---------------------------
    # SUMMARY
    # ---------------------------

    print("\n" + "=" * 50)

    print(
        f"Games: {len(df):,}"
    )

    print(
        f"Duplicates removed: "
        f"{duplicates_removed:,}"
    )

    print(
        f"Date range: "
        f"{df['date'].min()} "
        f"-> "
        f"{df['date'].max()}"
    )

    white_elo_pct = (
        df["white_elo"]
        .notna()
        .mean()
        * 100
    )

    black_elo_pct = (
        df["black_elo"]
        .notna()
        .mean()
        * 100
    )

    print(
        f"White Elo available: "
        f"{white_elo_pct:.1f}%"
    )

    print(
        f"Black Elo available: "
        f"{black_elo_pct:.1f}%"
    )

    print("\nResult distribution")

    print(
        df["result"]
        .value_counts()
        .sort_index()
    )

    print("=" * 50)


if __name__ == "__main__":
    main()