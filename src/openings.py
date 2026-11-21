
from src.player_service import get_connection


def get_openings_stats():

    con = get_connection()

    total_openings = con.execute(
        """
        SELECT COUNT(DISTINCT eco)
        FROM games_matched
        WHERE eco IS NOT NULL
        """
    ).fetchone()[0]

    most_played = con.execute(
        """
        SELECT
            eco,
            COUNT(*) AS games
        FROM games_matched
        WHERE eco IS NOT NULL
        GROUP BY eco
        ORDER BY games DESC
        LIMIT 1
        """
    ).fetchone()

    white_best = con.execute(
        """
        SELECT
            eco,
            ROUND(
                AVG(
                    CASE
                        WHEN result_score = 2
                        THEN 1
                        ELSE 0
                    END
                ) * 100,
                2
            ) AS white_win_rate,
            COUNT(*) AS games
        FROM games_matched
        WHERE eco IS NOT NULL
        GROUP BY eco
        HAVING COUNT(*) >= 100
        ORDER BY white_win_rate DESC
        LIMIT 1
        """
    ).fetchone()

    highest_draw = con.execute(
        """
        SELECT
            eco,
            ROUND(
                AVG(
                    CASE
                        WHEN result_score = 1
                        THEN 1
                        ELSE 0
                    END
                ) * 100,
                2
            ) AS draw_rate,
            COUNT(*) AS games
        FROM games_matched
        WHERE eco IS NOT NULL
        GROUP BY eco
        HAVING COUNT(*) >= 100
        ORDER BY draw_rate DESC
        LIMIT 1
        """
    ).fetchone()

    con.close()

    return {
        "total_openings": total_openings,

        "most_played": {
            "eco": most_played[0],
            "games": most_played[1]
        },

        "white_best": {
            "eco": white_best[0],
            "win_rate": white_best[1]
        },

        "highest_draw": {
            "eco": highest_draw[0],
            "draw_rate": highest_draw[1]
        }
    }


def get_top_openings(
    limit: int = 100
):

    con = get_connection()

    rows = con.execute(
        """
        SELECT
            eco,

            COUNT(*) AS games,

            ROUND(
                AVG(
                    CASE
                        WHEN result_score = 2
                        THEN 1
                        ELSE 0
                    END
                ) * 100,
                2
            ) AS white_win_rate,

            ROUND(
                AVG(
                    CASE
                        WHEN result_score = 1
                        THEN 1
                        ELSE 0
                    END
                ) * 100,
                2
            ) AS draw_rate,

            ROUND(
                AVG(
                    CASE
                        WHEN result_score = 0
                        THEN 1
                        ELSE 0
                    END
                ) * 100,
                2
            ) AS black_win_rate

        FROM games_matched

        WHERE eco IS NOT NULL

        GROUP BY eco

        HAVING COUNT(*) >= 50

        ORDER BY games DESC

        LIMIT ?
        """,
        [limit]
    ).fetchall()

    con.close()

    return [
        {
            "eco": row[0],
            "games": row[1],
            "white_win_rate": row[2],
            "draw_rate": row[3],
            "black_win_rate": row[4]
        }
        for row in rows
    ]


def get_opening_details(
    eco: str
):

    con = get_connection()

    row = con.execute(
        """
        SELECT
            eco,

            COUNT(*) AS games,

            ROUND(
                AVG(
                    CASE
                        WHEN result_score = 2
                        THEN 1
                        ELSE 0
                    END
                ) * 100,
                2
            ) AS white_win_rate,

            ROUND(
                AVG(
                    CASE
                        WHEN result_score = 1
                        THEN 1
                        ELSE 0
                    END
                ) * 100,
                2
            ) AS draw_rate,

            ROUND(
                AVG(
                    CASE
                        WHEN result_score = 0
                        THEN 1
                        ELSE 0
                    END
                ) * 100,
                2
            ) AS black_win_rate,

            ROUND(
                AVG(white_elo),
                0
            ) AS avg_white_elo,

            ROUND(
                AVG(black_elo),
                0
            ) AS avg_black_elo

        FROM games_matched

        WHERE eco = ?

        GROUP BY eco
        """,
        [eco]
    ).fetchone()

    con.close()

    if row is None:
        return None

    return {
        "eco": row[0],
        "games": row[1],
        "white_win_rate": row[2],
        "draw_rate": row[3],
        "black_win_rate": row[4],
        "avg_white_elo": row[5],
        "avg_black_elo": row[6]
    }
def get_opening_top_players(
    eco: str
):

    con = get_connection()

    rows = con.execute(
        """
        SELECT
            player,
            MAX(rating) AS peak_rating
        FROM (

            SELECT
                white AS player,
                white_elo AS rating
            FROM games_matched
            WHERE eco = ?

            UNION ALL

            SELECT
                black AS player,
                black_elo AS rating
            FROM games_matched
            WHERE eco = ?

        )

        GROUP BY player

        HAVING peak_rating IS NOT NULL

        ORDER BY peak_rating DESC

        LIMIT 5
        """,
        [eco, eco]
    ).fetchall()

    con.close()

    return [
        {
            "name": row[0],
            "rating": row[1]
        }
        for row in rows
    ]

def get_opening_top_player(
    eco: str
):

    con = get_connection()

    row = con.execute(
        """
        SELECT
            player,
            MAX(rating) AS peak_rating,
            COUNT(*) AS games_with_opening
        FROM (

            SELECT
                white AS player,
                white_elo AS rating
            FROM games_matched
            WHERE eco = ?

            UNION ALL

            SELECT
                black AS player,
                black_elo AS rating
            FROM games_matched
            WHERE eco = ?

        ) t

        WHERE
            rating IS NOT NULL
            AND rating < 2900

        GROUP BY player

        HAVING COUNT(*) >= 5

        ORDER BY
            games_with_opening DESC,
            peak_rating DESC

        LIMIT 1
        """,
        [eco, eco]
    ).fetchone()

    con.close()

    if not row:
        return None

    return {
        "name": row[0],
        "rating": row[1],
        "games": row[2]
    }