from pathlib import Path
import re
import unicodedata
import xml.etree.ElementTree as ET

import duckdb
import pandas as pd

from src.config import DB_PATH, PROCESSED


# =====================================================
# NAME NORMALIZATION
# =====================================================

def normalize_name(name: str) -> str:
    """
    Normalize chess player names.
    """

    if not name:
        return ""

    name = str(name).strip()

    if "," in name:

        parts = [p.strip() for p in name.split(",")]

        if len(parts) == 2:
            name = f"{parts[1]} {parts[0]}"

    name = (
        unicodedata
        .normalize("NFKD", name)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    name = name.lower()

    name = re.sub(
        r"[^a-z0-9 ]",
        " ",
        name
    )

    name = " ".join(name.split())

    return name


# =====================================================
# PARSE FIDE XML
# =====================================================

def parse_fide_xml() -> pd.DataFrame:

    xml_file = (
        Path("data/raw/fide")
        / "standard_rating_list.xml"
    )

    if not xml_file.exists():
        raise FileNotFoundError(
            f"Missing file: {xml_file}"
        )

    print(f"Reading {xml_file.name}")

    rows = []

    for _, elem in ET.iterparse(xml_file):

        if elem.tag.lower() == "player":

            row = {}

            for child in elem:
                row[
                    child.tag.lower()
                ] = child.text

            rows.append(row)

            elem.clear()

    df = pd.DataFrame(rows)

    df["normalized_name"] = (
        df["name"]
        .fillna("")
        .apply(normalize_name)
    )

    output = (
        PROCESSED
        / "fide_players.parquet"
    )

    df.to_parquet(
        output,
        index=False
    )

    con = duckdb.connect(DB_PATH)

    con.execute("""
        CREATE OR REPLACE TABLE fide_players
        AS
        SELECT *
        FROM 'data/processed/fide_players.parquet'
    """)

    print(
        f"Players found: {len(df):,}"
    )

    return df


# =====================================================
# MATCH PLAYERS
# =====================================================

def match_players():

    con = duckdb.connect(DB_PATH)

    games = con.sql("""
        SELECT *
        FROM games
    """).df()

    players = con.sql("""
        SELECT *
        FROM fide_players
    """).df()

    print(
        f"Games loaded: {len(games):,}"
    )

    print(
        f"Players loaded: {len(players):,}"
    )

    # -----------------------------------
    # Build lookup tables
    # -----------------------------------

    fide_lookup = {}

    if "fideid" in players.columns:

        fide_lookup = dict(
            zip(
                players["fideid"].astype(str),
                players["fideid"].astype(str)
            )
        )

    name_lookup = dict(
        zip(
            players["normalized_name"],
            players["fideid"].astype(str)
        )
    )

    # -----------------------------------
    # White player matching
    # -----------------------------------

    white_ids = []

    for _, row in games.iterrows():

        fide_id = row.get(
            "white_fide_id"
        )

        if pd.notna(fide_id):

            fide_id = str(fide_id)

            if fide_id in fide_lookup:

                white_ids.append(
                    fide_id
                )

                continue

        name = normalize_name(
            row["white"]
        )

        white_ids.append(
            name_lookup.get(name)
        )

    # -----------------------------------
    # Black player matching
    # -----------------------------------

    black_ids = []

    for _, row in games.iterrows():

        fide_id = row.get(
            "black_fide_id"
        )

        if pd.notna(fide_id):

            fide_id = str(fide_id)

            if fide_id in fide_lookup:

                black_ids.append(
                    fide_id
                )

                continue

        name = normalize_name(
            row["black"]
        )

        black_ids.append(
            name_lookup.get(name)
        )

    games["white_id"] = white_ids
    games["black_id"] = black_ids

    # -----------------------------------
    # Match statistics
    # -----------------------------------

    both_matched = (
        games["white_id"].notna()
        &
        games["black_id"].notna()
    )

    match_rate = (
        both_matched.mean() * 100
    )

    print(
        f"\nMatch rate: "
        f"{match_rate:.2f}%"
    )

    # -----------------------------------
    # Unmatched players
    # -----------------------------------

    unmatched_white = (
        games.loc[
            games["white_id"].isna(),
            "white"
        ]
        .value_counts()
        .head(20)
    )

    print(
        "\nTop unmatched white players:"
    )

    print(unmatched_white)

    # -----------------------------------
    # Save games table
    # -----------------------------------

    output = (
        PROCESSED
        / "games_matched.parquet"
    )

    games.to_parquet(
        output,
        index=False
    )

    con.execute("""
        CREATE OR REPLACE TABLE games_matched
        AS
        SELECT *
        FROM 'data/processed/games_matched.parquet'
    """)

    print(
        "\nSaved games_matched table."
    )


# =====================================================
# MAIN
# =====================================================

def main():

    parse_fide_xml()

    match_players()


if __name__ == "__main__":
    main()