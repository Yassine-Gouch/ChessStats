from collections import defaultdict, deque

import duckdb
import pandas as pd

from src.config import DB_PATH, PROCESSED


def average_form(results: deque) -> float:
    """
    Average score in history.

    Win = 1
    Draw = 0.5
    Loss = 0
    """

    if len(results) == 0:
        return 0.5

    return sum(results) / len(results)


def build_features() -> pd.DataFrame:

    con = duckdb.connect(DB_PATH)

    games = con.sql("""
    SELECT *
    FROM games_matched
    ORDER BY date
    """).df()

    print(
        f"Games loaded: {len(games):,}"
    )

    # -------------------------
    # Player state
    # -------------------------

    player_games = defaultdict(int)

    form10 = defaultdict(
        lambda: deque(maxlen=10)
    )

    form30 = defaultdict(
        lambda: deque(maxlen=30)
    )
    rating_history_10 = defaultdict(
        lambda: deque(maxlen=10)
    )

    rating_history_30 = defaultdict(
        lambda: deque(maxlen=30)
    )
    last_game_date = {}

    # -------------------------
    # Head-to-head
    # -------------------------

    h2h_games = defaultdict(int)

    h2h_white_points = defaultdict(float)

    # -------------------------
    # ECO history
    # -------------------------

    eco_games = defaultdict(int)

    eco_white_points = defaultdict(float)

    eco_draws = defaultdict(int)
    # -------------------------
    # Strong Opponents
    # -------------------------

    vs_2700_scores = defaultdict(list)

    #
    white_side_scores = defaultdict(list)

    black_side_scores = defaultdict(list)

    rows = []

    for row in games.itertuples():

        white_id = row.white_id
        black_id = row.black_id

        if pd.isna(white_id):
            continue

        if pd.isna(black_id):
            continue

        white_elo = row.white_elo
        black_elo = row.black_elo

        if pd.isna(white_elo):
            continue

        if pd.isna(black_elo):
            continue

        # -------------------------
        # Experience
        # -------------------------

        white_games_count = (
            player_games[white_id]
        )

        black_games_count = (
            player_games[black_id]
        )

        # -------------------------
        # Form
        # -------------------------

        white_form_10 = average_form(
            form10[white_id]
        )

        black_form_10 = average_form(
            form10[black_id]
        )

        white_form_30 = average_form(
            form30[white_id]
        )

        black_form_30 = average_form(
            form30[black_id]
        )

        # -------------------------
        # Head-to-head
        # -------------------------

        pair = (
            white_id,
            black_id
        )

        h2h_count = h2h_games[pair]

        if h2h_count > 0:

            h2h_white_score = (
                h2h_white_points[pair]
                /
                h2h_count
            )

        else:

            h2h_white_score = 0.5

        # -------------------------
        # ECO historical stats
        # -------------------------

        eco_code = row.eco

        eco_count = eco_games[eco_code]

        if eco_count > 0:

            eco_white_score = (
                eco_white_points[eco_code]
                /
                eco_count
            )

            eco_draw_rate = (
                eco_draws[eco_code]
                /
                eco_count
            )

        else:

            eco_white_score = 0.5

            eco_draw_rate = 0.25

        # -------------------------
        # Days since last game
        # -------------------------

        current_date = row.date
        if white_id in last_game_date:

            days_white = (
                current_date
                -
                last_game_date[
                    white_id
                ]
            ).days

        else:

            days_white = -1

        if black_id in last_game_date:

            days_black = (
                current_date
                -
                last_game_date[
                    black_id
                ]
            ).days

        else:

            days_black = -1

        # -------------------------
        # Save feature row
        # -------------------------
        if rating_history_10[white_id]:
            white_rating_trend_10 = (
                white_elo -
                rating_history_10[white_id][0]
            )
        else:
            white_rating_trend_10 = 0

        if rating_history_10[black_id]:
            black_rating_trend_10 = (
                black_elo -
                rating_history_10[black_id][0]
            )
        else:
            black_rating_trend_10 = 0

        if rating_history_30[white_id]:
            white_rating_trend_30 = (
                white_elo -
                rating_history_30[white_id][0]
            )
        else:
            white_rating_trend_30 = 0

        if rating_history_30[black_id]:
            black_rating_trend_30 = (
                black_elo -
                rating_history_30[black_id][0]
            )
        else:
            black_rating_trend_30 = 0

        white_wins_last10 = sum(
            1
            for x in form10[white_id]
            if x == 1.0
        )

        white_draws_last10 = sum(
            1
            for x in form10[white_id]
            if x == 0.5
        )

        white_losses_last10 = sum(
            1
            for x in form10[white_id]
            if x == 0.0
        )

        black_wins_last10 = sum(
            1
            for x in form10[black_id]
            if x == 1.0
        )

        black_draws_last10 = sum(
            1
            for x in form10[black_id]
            if x == 0.5
        )

        black_losses_last10 = sum(
            1
            for x in form10[black_id]
            if x == 0.0
        )
        if vs_2700_scores[white_id]:

            white_score_vs_2700 = (
                sum(vs_2700_scores[white_id])
                /
                len(vs_2700_scores[white_id])
            )

        else:

            white_score_vs_2700 = 0.5


        if vs_2700_scores[black_id]:

            black_score_vs_2700 = (
                sum(vs_2700_scores[black_id])
                /
                len(vs_2700_scores[black_id])
            )

        else:

            black_score_vs_2700 = 0.5


        if white_side_scores[white_id]:

            white_score_as_white = (
                sum(white_side_scores[white_id])
                /
                len(white_side_scores[white_id])
            )

        else:

            white_score_as_white = 0.5


        if black_side_scores[black_id]:

            black_score_as_black = (
                sum(black_side_scores[black_id])
                /
                len(black_side_scores[black_id])
            )

        else:

            black_score_as_black = 0.5

        rows.append({
            "white_wins_last10":
                white_wins_last10,

            "white_draws_last10":
                white_draws_last10,

            "white_losses_last10":
                white_losses_last10,

            "black_wins_last10":
                black_wins_last10,

            "black_draws_last10":
                black_draws_last10,

            "black_losses_last10":
                black_losses_last10,

            "white_rating_trend_10":
                white_rating_trend_10,

            "black_rating_trend_10":
                black_rating_trend_10,

            "white_rating_trend_30":
                white_rating_trend_30,

            "black_rating_trend_30":
                black_rating_trend_30,

            "game_id":
                row.game_id,

            "date":
                row.date,

            "white_id":
                white_id,

            "black_id":
                black_id,

            "elo_white":
                white_elo,

            "elo_black":
                black_elo,

            "elo_diff":
                white_elo
                -
                black_elo,

            "elo_mean":
                (
                    white_elo
                    +
                    black_elo
                ) / 2,

            "white_games_count":
                white_games_count,

            "black_games_count":
                black_games_count,

            "white_form_10":
                white_form_10,

            "black_form_10":
                black_form_10,

            "white_form_30":
                white_form_30,

            "black_form_30":
                black_form_30,

            "days_since_last_game_white":
                days_white,

            "days_since_last_game_black":
                days_black,

            "h2h_games":
                h2h_count,

            "h2h_white_score":
                h2h_white_score,

            "eco_games":
                eco_count,

            "eco_white_score":
                eco_white_score,

            "eco_draw_rate":
                eco_draw_rate,

            "y":
                row.result_score,

            "white_score_vs_2700":
                white_score_vs_2700,

            "black_score_vs_2700":
                black_score_vs_2700,

            "white_score_as_white":
                white_score_as_white,

            "black_score_as_black":
                black_score_as_black
        })

        # -------------------------
        # Convert result
        # -------------------------

        if row.result_score == 2:

            white_score = 1.0
            black_score = 0.0

        elif row.result_score == 1:

            white_score = 0.5
            black_score = 0.5

        else:

            white_score = 0.0
            black_score = 1.0

        # -------------------------
        # Update H2H
        # -------------------------

        h2h_games[pair] += 1

        h2h_white_points[pair] += white_score

        # Strong opponents

        if black_elo >= 2700:

            vs_2700_scores[white_id].append(
                white_score
            )

        if white_elo >= 2700:

            vs_2700_scores[black_id].append(
                black_score
            )
       

        # -------------------------
        # Update ECO stats
        # -------------------------

        eco_games[eco_code] += 1

        eco_white_points[eco_code] += white_score

        if row.result_score == 1:

            eco_draws[eco_code] += 1

        # -------------------------
        # UPDATE STATE
        # IMPORTANT:
        # AFTER feature creation
        # -------------------------

        form10[white_id].append(
            white_score
        )

        form10[black_id].append(
            black_score
        )

        form30[white_id].append(
            white_score
        )

        form30[black_id].append(
            black_score
        )
        rating_history_10[white_id].append(
            white_elo
        )

        rating_history_10[black_id].append(
            black_elo
        )

        rating_history_30[white_id].append(
            white_elo
        )

        rating_history_30[black_id].append(
            black_elo
        )
        white_side_scores[white_id].append(
            white_score
        )

        black_side_scores[black_id].append(
            black_score
        )
        

        player_games[white_id] += 1

        player_games[black_id] += 1

        last_game_date[
            white_id
        ] = current_date

        last_game_date[
            black_id
        ] = current_date

    print("Loop finished")

    features = pd.DataFrame(rows)
    output = (
        PROCESSED /
        "features.parquet"
    )

    features.to_parquet(
        output,
        index=False
    )

    con.execute("""
    CREATE OR REPLACE TABLE features
    AS
    SELECT *
    FROM 'data/processed/features.parquet'
    """)

    print(
        f"\nFeature rows: {len(features):,}"
    )

    print(
        "\nColumns:\n"
    )

    print(
        features.columns.tolist()
    )

    print(
        "\nSample:"
    )

    print(
        features.head()
    )

    return features


def main():

    build_features()


if __name__ == "__main__":
    main()