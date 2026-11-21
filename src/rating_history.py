import duckdb
import pandas as pd

from src.config import DB_PATH, PROCESSED


def build_rating_history():

    con = duckdb.connect(DB_PATH)

    games = con.sql("""
        SELECT
            date,
            white_id,
            black_id,
            white,
            black,
            white_elo,
            black_elo
        FROM games_matched
    """).df()

    white = games[
        [
            "date",
            "white_id",
            "white",
            "white_elo"
        ]
    ].rename(
        columns={
            "white_id": "player_id",
            "white": "player_name",
            "white_elo": "rating"
        }
    )

    black = games[
        [
            "date",
            "black_id",
            "black",
            "black_elo"
        ]
    ].rename(
        columns={
            "black_id": "player_id",
            "black": "player_name",
            "black_elo": "rating"
        }
    )

    rating_history = pd.concat(
        [white, black],
        ignore_index=True
    )

    rating_history = rating_history.dropna(
        subset=[
            "player_id",
            "rating"
        ]
    )

    rating_history = (
        rating_history
        .sort_values(
            ["player_id", "date"]
        )
        .drop_duplicates(
            subset=[
                "player_id",
                "date",
                "rating"
            ]
        )
    )

    output = (
        PROCESSED /
        "rating_history.parquet"
    )

    rating_history.to_parquet(
        output,
        index=False
    )

    con.execute("""
        CREATE OR REPLACE TABLE rating_history
        AS
        SELECT *
        FROM 'data/processed/rating_history.parquet'
    """)

    print(
        f"Rating history rows: "
        f"{len(rating_history):,}"
    )

    top_players = (
        rating_history
        .groupby("player_name")
        .size()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    print("\nMost active players:\n")
    print(top_players)


def main():
    build_rating_history()


if __name__ == "__main__":
    main()