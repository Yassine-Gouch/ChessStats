import duckdb


DB_PATH = "data/processed/chess_portfolio.duckdb"


def get_connection():

    return duckdb.connect(DB_PATH)


# =====================================================
# PLAYER SEARCH
# =====================================================

def search_player(
    query: str,
    limit: int = 10
):

    con = get_connection()

    sql = """
    SELECT
        fideid,
        name,
        country,
        title,
        rating
    FROM fide_players
    WHERE normalized_name ILIKE ?
       OR name ILIKE ?
    ORDER BY rating DESC
    LIMIT ?
    """

    df = con.execute(
        sql,
        [
            f"%{query.lower()}%",
            f"%{query}%",
            limit
        ]
    ).fetchdf()

    # FastAPI ne supporte pas NaN
    df = df.fillna("")

    results = df.to_dict(
        "records"
    )

    con.close()

    return results


def resolve_player(
    query: str
):

    results = search_player(
        query,
        limit=1
    )

    if not results:

        return None

    return results[0]


# =====================================================
# PROFILE
# =====================================================

def get_player_games_count(
    player_name: str
):

    con = get_connection()

    surname = player_name.split(",")[0]

    sql = """
    SELECT COUNT(*) AS games
    FROM games_matched
    WHERE white ILIKE ?
       OR black ILIKE ?
    """

    result = con.execute(
        sql,
        [
            f"%{surname}%",
            f"%{surname}%"
        ]
    ).fetchone()

    con.close()

    return int(result[0])


def get_player_last_elo(
    player_name: str
):

    con = get_connection()

    surname = player_name.split(",")[0]

    sql = """
    SELECT *
    FROM (

        SELECT
            white_elo AS elo,
            date
        FROM games_matched
        WHERE white ILIKE ?

        UNION ALL

        SELECT
            black_elo AS elo,
            date
        FROM games_matched
        WHERE black ILIKE ?

    )

    ORDER BY date DESC

    LIMIT 1
    """

    result = con.execute(
        sql,
        [
            f"%{surname}%",
            f"%{surname}%"
        ]
    ).fetchone()

    con.close()

    if result is None:
        return None

    return int(result[0])


def get_player_profile(
    query: str
):

    player = resolve_player(
        query
    )

    if player is None:
        return None

    return {

        "fideid":
            player["fideid"],

        "name":
            player["name"],

        "country":
            player["country"],

        "title":
            player["title"],

        "rating":
            int(player["rating"])
            if player["rating"] is not None
            else None,

        "games":
            get_player_games_count(
                player["name"]
            ),

        "last_elo":
            get_player_last_elo(
                player["name"]
            )
    }


# =====================================================
# OPENINGS
# =====================================================

def get_player_openings(
    query: str,
    limit: int = 10
):

    player = resolve_player(
        query
    )

    if player is None:
        return []

    surname = (
        player["name"]
        .split(",")[0]
        .strip()
    )

    con = get_connection()

    sql = """
    SELECT
        eco,
        COUNT(*) AS games

    FROM games_matched

    WHERE
    (
        white ILIKE ?
        OR black ILIKE ?
    )
    AND eco IS NOT NULL

    GROUP BY eco

    ORDER BY games DESC

    LIMIT ?
    """

    df = con.execute(
        sql,
        [
            f"%{surname}%",
            f"%{surname}%",
            limit
        ]
    ).fetchdf()

    results = df.to_dict(
        "records"
    )

    con.close()

    return results


# =====================================================
# HEAD TO HEAD
# =====================================================

def get_head_to_head(
    player_a: str,
    player_b: str
):

    profile_a = get_player_profile(
        player_a
    )

    profile_b = get_player_profile(
        player_b
    )

    if (
        profile_a is None
        or
        profile_b is None
    ):
        return {
            "games": 0,
            "player_a_wins": 0,
            "draws": 0,
            "player_b_wins": 0
        }

    surname_a = (
        profile_a["name"]
        .split(",")[0]
        .strip()
    )

    surname_b = (
        profile_b["name"]
        .split(",")[0]
        .strip()
    )

    con = get_connection()

    sql = """
    SELECT

        COUNT(*) AS games,

        SUM(
            CASE
                WHEN (
                    white ILIKE ?
                    AND result = '1-0'
                )
                OR (
                    black ILIKE ?
                    AND result = '0-1'
                )
                THEN 1
                ELSE 0
            END
        ) AS player_a_wins,

        SUM(
            CASE
                WHEN result = '1/2-1/2'
                THEN 1
                ELSE 0
            END
        ) AS draws,

        SUM(
            CASE
                WHEN (
                    white ILIKE ?
                    AND result = '1-0'
                )
                OR (
                    black ILIKE ?
                    AND result = '0-1'
                )
                THEN 1
                ELSE 0
            END
        ) AS player_b_wins

    FROM games_matched

    WHERE

    (
        white ILIKE ?
        AND black ILIKE ?
    )

    OR

    (
        white ILIKE ?
        AND black ILIKE ?
    )
    """

    result = con.execute(
        sql,
        [
            f"%{surname_a}%",
            f"%{surname_a}%",

            f"%{surname_b}%",
            f"%{surname_b}%",

            f"%{surname_a}%",
            f"%{surname_b}%",

            f"%{surname_b}%",
            f"%{surname_a}%"
        ]
    ).fetchone()

    con.close()

    return {

        "games":
            int(result[0] or 0),

        "player_a_wins":
            int(result[1] or 0),

        "draws":
            int(result[2] or 0),

        "player_b_wins":
            int(result[3] or 0)

    }
# =====================================================
# COMPARE
# =====================================================

def compare_players(
    player_a: str,
    player_b: str
):

    profile_a = get_player_profile(
        player_a
    )

    profile_b = get_player_profile(
        player_b
    )

    if (
        profile_a is None
        or
        profile_b is None
    ):
        return None

    return {

        "player_a":
            profile_a,

        "player_b":
            profile_b,

        "elo_diff":
            profile_a["rating"]
            -
            profile_b["rating"],

        "head_to_head":
            get_head_to_head(
                player_a,
                player_b
            )
    }

# =====================================================
# RATING HISTORY
# =====================================================

def get_player_rating_history(
    query: str,
    limit: int = 200
):

    player = resolve_player(
        query
    )

    if player is None:
        return []

    surname = (
        player["name"]
        .split(",")[0]
        .strip()
    )

    con = get_connection()

    sql = """
    SELECT
        date,
        rating

    FROM rating_history

    WHERE player_name ILIKE ?

    ORDER BY date
    """

    df = con.execute(
        sql,
        [
            f"%{surname}%"
        ]
    ).fetchdf()

    results = []

    for _, row in df.iterrows():

        results.append({

            "date":
                str(row["date"])[:10],

            "rating":
                int(row["rating"])

        })

    con.close()

    return results[-limit:]
# =====================================================
# DEMO
# =====================================================

def demo():

    print(
        search_player(
            "magnus"
        )
    )

    print()

    print(
        get_player_profile(
            "magnus"
        )
    )

    print()

    print(
        get_player_openings(
            "magnus"
        )
    )

    print()

    print(
        compare_players(
            "magnus",
            "hikaru"
        )
    )

    print()

    print(
        get_head_to_head(
            "magnus",
            "hikaru"
        )
    )


if __name__ == "__main__":

    demo()