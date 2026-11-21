from pathlib import Path

import joblib
import pandas as pd

from src.player_service import (
    get_connection,
    get_player_profile,
    get_head_to_head
)


MODEL_PATH = Path(
    "models/xgboost.joblib"
)


def load_model():

    model = joblib.load(
        MODEL_PATH
    )

    return model


def predict_features(
    features_dict
):

    model = load_model()

    X = pd.DataFrame(
        [features_dict]
    )

    prediction = model.predict(
        X
    )[0]

    probabilities = (
        model.predict_proba(X)[0]
    )

    labels = {

        0: "Black Win",
        1: "Draw",
        2: "White Win"
    }

    return {

        "prediction":
            labels[prediction],

        "black_win":
            round(
                float(probabilities[0]) * 100,
                2
            ),

        "draw":
            round(
                float(probabilities[1]) * 100,
                2
            ),

        "white_win":
            round(
                float(probabilities[2]) * 100,
                2
            )
    }
from datetime import datetime

def get_days_since_last_game(
    player_id: str
):

    con = get_connection()

    result = con.execute(
        """
        SELECT date
        FROM games_matched
        WHERE white_id = ?
           OR black_id = ?
        ORDER BY date DESC
        LIMIT 1
        """,
        [
            player_id,
            player_id
        ]
    ).fetchone()

    con.close()

    if result is None:
        return -1

    last_date = result[0]

    return (
        datetime.now() -
        last_date
    ).days


#####
def get_side_score(
    player_id: str,
    side: str
):
    con = get_connection()

    if side == "white":
        games = con.execute(
            """
            SELECT result_score
            FROM games_matched
            WHERE white_id = ?
            """,
            [player_id]
        ).fetchall()

    else:
        games = con.execute(
            """
            SELECT result_score
            FROM games_matched
            WHERE black_id = ?
            """,
            [player_id]
        ).fetchall()

    con.close()

    if not games:
        return 0.5

    scores = []

    for (result,) in games:

        if side == "white":

            if result == 2:
                scores.append(1)

            elif result == 1:
                scores.append(0.5)

            else:
                scores.append(0)

        else:

            if result == 0:
                scores.append(1)

            elif result == 1:
                scores.append(0.5)

            else:
                scores.append(0)

    return sum(scores) / len(scores)

def get_last10_stats(
    player_id: str
):

    con = get_connection()

    games = con.execute(
        """
        SELECT
            white_id,
            black_id,
            result_score
        FROM games_matched
        WHERE white_id = ?
           OR black_id = ?
        ORDER BY date DESC
        LIMIT 10
        """,
        [
            player_id,
            player_id
        ]
    ).fetchall()

    con.close()

    wins = 0
    draws = 0
    losses = 0

    for white_id, black_id, result in games:

        if white_id == player_id:

            if result == 2:
                wins += 1

            elif result == 1:
                draws += 1

            else:
                losses += 1

        else:

            if result == 0:
                wins += 1

            elif result == 1:
                draws += 1

            else:
                losses += 1

    return {
        "wins": wins,
        "draws": draws,
        "losses": losses
    }

def get_score_vs_2700(
    player_id: str
):

    con = get_connection()

    games = con.execute(
        """
        SELECT
            white_id,
            black_id,
            white_elo,
            black_elo,
            result_score
        FROM games_matched
        WHERE white_id = ?
           OR black_id = ?
        """,
        [
            player_id,
            player_id
        ]
    ).fetchall()

    con.close()

    scores = []

    for (
        white_id,
        black_id,
        white_elo,
        black_elo,
        result
    ) in games:

        if white_id == player_id:

            if (
                black_elo is None
                or black_elo < 2700
            ):
                continue

            if result == 2:
                scores.append(1.0)

            elif result == 1:
                scores.append(0.5)

            else:
                scores.append(0.0)

        else:

            if (
                white_elo is None
                or white_elo < 2700
            ):
                continue

            if result == 0:
                scores.append(1.0)

            elif result == 1:
                scores.append(0.5)

            else:
                scores.append(0.0)

    if not scores:
        return 0.5

    return sum(scores) / len(scores)

def get_player_form(
    player_id: str,
    last_n: int = 10
):

    con = get_connection()

    sql = """
    SELECT
        white_id,
        black_id,
        result_score
    FROM games_matched
    WHERE white_id = ?
       OR black_id = ?
    ORDER BY date DESC
    LIMIT ?
    """

    games = con.execute(
        sql,
        [
            player_id,
            player_id,
            last_n
        ]
    ).fetchall()

    con.close()

    if not games:
        return 0.5

    scores = []

    for white_id, black_id, result in games:

        if white_id == player_id:

            if result == 2:
                scores.append(1.0)

            elif result == 1:
                scores.append(0.5)

            else:
                scores.append(0.0)

        else:

            if result == 0:
                scores.append(1.0)

            elif result == 1:
                scores.append(0.5)

            else:
                scores.append(0.0)

    return sum(scores) / len(scores)

def get_rating_trend(
    player_id: str,
    games_back: int
):

    con = get_connection()

    games = con.execute(
        """
        SELECT
            white_id,
            black_id,
            white_elo,
            black_elo
        FROM games_matched
        WHERE white_id = ?
           OR black_id = ?
        ORDER BY date DESC
        LIMIT ?
        """,
        [
            player_id,
            player_id,
            games_back + 1
        ]
    ).fetchall()

    con.close()

    if len(games) < 2:
        return 0

    latest = games[0]

    if latest[0] == player_id:
        current_rating = latest[2]
    else:
        current_rating = latest[3]

    oldest = games[-1]

    if oldest[0] == player_id:
        old_rating = oldest[2]
    else:
        old_rating = oldest[3]

    return current_rating - old_rating

def predict_match(
    white_name: str,
    black_name: str
):
    
    white = get_player_profile(
        white_name
    )

    black = get_player_profile(
        black_name
    )

    if white is None:

        return {
            "error":
                f"Player not found: {white_name}"
        }

    if black is None:

        return {
            "error":
                f"Player not found: {black_name}"
        }

    days_white = get_days_since_last_game(
        white["fideid"]
    )

    days_black = get_days_since_last_game(
        black["fideid"]
    )

    white_form_10 = get_player_form(
        white["fideid"],
        10
    )

    black_form_10 = get_player_form(
        black["fideid"],
        10
    )

    white_form_30 = get_player_form(
        white["fideid"],
        30
    )

    black_form_30 = get_player_form(
        black["fideid"],
        30
    )
    
    white_score_as_white = get_side_score(
        white["fideid"],
        "white"
    )

    black_score_as_black = get_side_score(
        black["fideid"],
        "black"
    )
    white_last10 = get_last10_stats(
        white["fideid"]
    )

    black_last10 = get_last10_stats(
        black["fideid"]
    )

    white_rating_trend_10 = get_rating_trend(
        white["fideid"],
        10
    )

    black_rating_trend_10 = get_rating_trend(
        black["fideid"],
        10
    )

    white_rating_trend_30 = get_rating_trend(
        white["fideid"],
        30
    )

    black_rating_trend_30 = get_rating_trend(
        black["fideid"],
        30
    )

    white_score_vs_2700 = get_score_vs_2700(
        white["fideid"]
    )

    black_score_vs_2700 = get_score_vs_2700(
        black["fideid"]
    )

    h2h = get_head_to_head(
        white_name,
        black_name
    )

    features = {

        "elo_white":
            white["rating"],

        "elo_black":
            black["rating"],

        "elo_diff":
            white["rating"]
            -
            black["rating"],

        "elo_mean":
            (
                white["rating"]
                +
                black["rating"]
            ) / 2,

        "white_games_count":
            white["games"],

        "black_games_count":
            black["games"],

        # Valeurs temporaires
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
            h2h["games"],

        "h2h_white_score":
        (
            h2h["player_a_wins"]
            +
            h2h["draws"] * 0.5
        )
        /
        max(h2h["games"], 1),

        # ECO temporaire
        "eco_games":
            1000,

        "eco_white_score":
            0.50,

        "eco_draw_rate":
            0.30,

        "white_rating_trend_10":
            white_rating_trend_10,

        "black_rating_trend_10":
            black_rating_trend_10,

        "white_rating_trend_30":
            white_rating_trend_30,

        "black_rating_trend_30":
            black_rating_trend_30,

        "white_wins_last10":
            white_last10["wins"],

        "white_draws_last10":
            white_last10["draws"],

        "white_losses_last10":
            white_last10["losses"],

        "black_wins_last10":
            black_last10["wins"],

        "black_draws_last10":
            black_last10["draws"],

        "black_losses_last10":
            black_last10["losses"],

        "white_score_vs_2700":
            white_score_vs_2700,
        "black_score_vs_2700":
            black_score_vs_2700,

        "white_score_as_white":
            white_score_as_white,

        "black_score_as_black":
            black_score_as_black
    }
    print(features)
    prediction = predict_features(
        features
    )

    return {

        "white":
            white["name"],

        "black":
            black["name"],

        "white_rating":
            white["rating"],

        "black_rating":
            black["rating"],

        "h2h_games":
            h2h["games"],

        **prediction
    }


def demo():

    result = predict_match(
        "magnus",
        "hikaru"
    )

    print(
        result
    )


if __name__ == "__main__":

    demo()