from pathlib import Path

import duckdb
import pandas as pd

from src.config import DB_PATH, PROCESSED


def build_tournaments():

    con = duckdb.connect(DB_PATH)

    games = con.sql("""
        SELECT *
        FROM games
    """).df()

    games["year"] = (
        games["date"]
        .dt.year
    )

    games["avg_game_elo"] = (
        games["white_elo"]
        +
        games["black_elo"]
    ) / 2

    tournaments = (
        games
        .groupby(
            [
                "event",
                "site",
                "year"
            ],
            dropna=False
        )
        .agg(
            start_date=(
                "date",
                "min"
            ),
            end_date=(
                "date",
                "max"
            ),
            games_count=(
                "game_id",
                "count"
            ),
            avg_elo=(
                "avg_game_elo",
                "mean"
            ),
            draw_rate=(
                "result",
                lambda s:
                (
                    s == "1/2-1/2"
                ).mean()
                * 100
            ),
            decisive_rate=(
                "result",
                lambda s:
                (
                    s != "1/2-1/2"
                ).mean()
                * 100
            )
        )
        .reset_index()
    )

    players_per_event = (
        games
        .groupby(
            [
                "event",
                "site",
                "year"
            ]
        )
        .apply(
            lambda g:
            len(
                set(g["white"])
                |
                set(g["black"])
            )
        )
        .reset_index(
            name="players_count"
        )
    )

    tournaments = (
        tournaments
        .merge(
            players_per_event,
            on=[
                "event",
                "site",
                "year"
            ],
            how="left"
        )
    )

    tournaments["avg_elo"] = (
        tournaments["avg_elo"]
        .round(1)
    )

    tournaments["draw_rate"] = (
        tournaments["draw_rate"]
        .round(2)
    )

    tournaments["decisive_rate"] = (
        tournaments["decisive_rate"]
        .round(2)
    )

    output = (
        PROCESSED
        / "tournaments.parquet"
    )

    tournaments.to_parquet(
        output,
        index=False
    )

    con.execute("""
        CREATE OR REPLACE TABLE tournaments
        AS
        SELECT *
        FROM 'data/processed/tournaments.parquet'
    """)

    print(
        f"Tournaments: {len(tournaments):,}"
    )

    print("\nTop 10 strongest tournaments:\n")

    strongest = (
        tournaments
        .sort_values(
            "avg_elo",
            ascending=False
        )
        .head(10)
    )

    print(
        strongest[
            [
                "event",
                "year",
                "avg_elo",
                "players_count",
                "games_count"
            ]
        ]
    )


def main():
    build_tournaments()


if __name__ == "__main__":
    main()