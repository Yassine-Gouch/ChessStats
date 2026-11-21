from src.player_service import get_connection


def get_tournaments_stats():

    con = get_connection()

    total_tournaments = con.execute(
        """
        SELECT COUNT(*)
        FROM tournaments
        """
    ).fetchone()[0]

    most_played = con.execute(
        """
        SELECT
            event,
            avg_elo
        FROM tournaments
        WHERE avg_elo < 3000
        ORDER BY avg_elo DESC
        LIMIT 1
        """
    ).fetchone()

    strongest = con.execute(
        """
        SELECT     
            event,
            avg_elo
        FROM tournaments
        WHERE avg_elo < 3000
        ORDER BY avg_elo DESC
        LIMIT 1
   
        """
    ).fetchone()

    average_elo = con.execute(
        """
        SELECT
            ROUND(
                AVG(avg_elo),
                0
            )
        FROM tournaments
        """
    ).fetchone()[0]

    con.close()

    return {
        "total_tournaments": total_tournaments,

        "most_played": {
            "event": most_played[0],
            "games": most_played[1]
        },

        "strongest": {
            "event": strongest[0],
            "avg_elo": strongest[1]
        },

        "average_elo": average_elo
    }


def get_top_tournaments(
    limit: int = 100
):

    con = get_connection()

    rows = con.execute(
        """
        SELECT
            event,
            year,
            games_count,
            players_count,
            avg_elo
        FROM tournaments
        ORDER BY games_count DESC
        LIMIT ?
        """,
        [limit]
    ).fetchall()

    con.close()

    return [
        {
            "event": row[0],
            "year": row[1],
            "games_count": row[2],
            "players_count": row[3],
            "avg_elo": row[4]
        }
        for row in rows
    ]


def get_tournament_details(
    event: str,
    year: int
):

    con = get_connection()

    row = con.execute(
        """
        SELECT
            event,
            site,
            year,
            start_date,
            end_date,
            games_count,
            players_count,
            avg_elo,
            draw_rate,
            decisive_rate
        FROM tournaments
        WHERE
            event = ?
            AND year = ?
        LIMIT 1
        """,
        [event, year]
    ).fetchone()

    con.close()

    if row is None:
        return None

    duration = (
        row[4] - row[3]
    ).days + 1

    if row[7] >= 2500:
        strength = "Elite"

    elif row[7] >= 2200:
        strength = "Strong"

    elif row[7] >= 1800:
        strength = "Average"

    else:
        strength = "Local"

    return {
        "event": row[0],
        "site": row[1],
        "year": row[2],
        "start_date": str(row[3]),
        "end_date": str(row[4]),
        "duration_days": duration,
        "games_count": row[5],
        "players_count": row[6],
        "avg_elo": row[7],
        "draw_rate": row[8],
        "decisive_rate": row[9],
        "strength": strength
    }