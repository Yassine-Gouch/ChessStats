from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.player_service import (
    search_player,
    get_player_profile,
    get_player_openings,
    compare_players,
    get_player_rating_history
)

from src.predict import (
    predict_match
)

from src.openings import (
    get_openings_stats,
    get_top_openings,
    get_opening_details,
    get_opening_top_player
)
from src.tournaments_service import (
    get_tournaments_stats,
    get_top_tournaments,
    get_tournament_details
)

app = FastAPI(
    title="ChessStats API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):

    white: str
    black: str


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return {
        "project": "ChessStats",
        "status": "running"
    }


# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# =====================================================
# PLAYER SEARCH
# =====================================================

@app.get("/players/search")
def player_search(
    q: str
):

    return search_player(q)


# =====================================================
# PLAYER PROFILE
# =====================================================

@app.get("/players/profile/{name}")
def player_profile(
    name: str
):

    return get_player_profile(name)


# =====================================================
# PLAYER OPENINGS
# =====================================================

@app.get("/players/openings/{name}")
def player_openings(
    name: str
):

    return get_player_openings(name)

@app.get("/openings/stats")
def openings_stats():
    return get_openings_stats()


@app.get("/openings/top")
def openings_top():
    return get_top_openings()


@app.get("/openings/{eco}")
def opening_details(
    eco: str
):
    return get_opening_details(
        eco.upper()
    )


@app.get("/openings/{eco}/top-player")
def opening_top_player(
    eco: str
):
    return get_opening_top_player(
        eco.upper()
    )


# =====================================================
# TOURNAMENTS
# =====================================================

@app.get("/tournaments/stats")
def tournaments_stats():

    return get_tournaments_stats()


@app.get("/tournaments/top")
def tournaments_top():

    return get_top_tournaments()


@app.get("/tournaments/{year}/{event}")
def tournament_details(
    year: int,
    event: str
):

    return get_tournament_details(
        event,
        year
    )
# =====================================================
# COMPARE PLAYERS
# =====================================================

@app.get(
    "/players/compare/{player_a}/{player_b}"
)
def compare(
    player_a: str,
    player_b: str
):

    return compare_players(
        player_a,
        player_b
    )


# =====================================================
# PREDICT
# =====================================================

@app.post("/predict")
def predict(
    request: PredictionRequest
):

    return predict_match(
        request.white,
        request.black
    )


#info
@app.get("/info")
def info():

    return {

        "project":
            "ChessStats",

        "model":
            "XGBoost",

        "accuracy":
            60.73,

        "games":
            483962,

        "players":
            569653
    }

# =====================================================
# RATING HISTORY
# =====================================================

@app.get("/players/rating-history/{name}")
def rating_history(
    name: str
):

    return get_player_rating_history(
        name
    )