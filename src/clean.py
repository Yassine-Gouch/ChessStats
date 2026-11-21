from pathlib import Path
from datetime import datetime

import duckdb
import pandas as pd

from src.config import DB_PATH


REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def build_data_quality_report() -> None:
    """
    Generate a data quality report
    from the games table.
    """

    con = duckdb.connect(DB_PATH)

    games = con.sql("""
        SELECT *
        FROM games
    """).df()

    total_games = len(games)

    print(f"Games loaded: {total_games:,}")

    # ==========================
    # Missing values
    # ==========================

    missing_white_elo = (
        games["white_elo"]
        .isna()
        .sum()
    )

    missing_black_elo = (
        games["black_elo"]
        .isna()
        .sum()
    )

    missing_white_name = (
        games["white"]
        .isna()
        .sum()
    )

    missing_black_name = (
        games["black"]
        .isna()
        .sum()
    )

    # ==========================
    # Elo validation
    # ==========================

    invalid_white_elo = (
        (
            games["white_elo"] < 1000
        )
        |
        (
            games["white_elo"] > 3500
        )
    ).sum()

    invalid_black_elo = (
        (
            games["black_elo"] < 1000
        )
        |
        (
            games["black_elo"] > 3500
        )
    ).sum()

    # ==========================
    # Dates
    # ==========================

    today = pd.Timestamp.now()

    future_dates = (
        games["date"] > today
    ).sum()

    missing_dates = (
        games["date"]
        .isna()
        .sum()
    )

    # ==========================
    # Results
    # ==========================

    allowed_results = {
        "1-0",
        "0-1",
        "1/2-1/2"
    }

    invalid_results = (
        ~games["result"]
        .isin(allowed_results)
    ).sum()

    # ==========================
    # Duplicate IDs
    # ==========================

    duplicate_game_ids = (
        games["game_id"]
        .duplicated()
        .sum()
    )

    # ==========================
    # Percentages
    # ==========================

    white_elo_pct = (
        games["white_elo"]
        .notna()
        .mean()
        * 100
    )

    black_elo_pct = (
        games["black_elo"]
        .notna()
        .mean()
        * 100
    )

    # ==========================
    # Report
    # ==========================

    report = f"""
# Chess Dataset Quality Report

Generated on: {datetime.now()}

---

## Dataset Overview

| Metric | Value |
|----------|----------|
| Total Games | {total_games:,} |
| Date Min | {games['date'].min()} |
| Date Max | {games['date'].max()} |

---

## Missing Values

| Check | Count |
|----------|----------|
| Missing White Name | {missing_white_name:,} |
| Missing Black Name | {missing_black_name:,} |
| Missing White Elo | {missing_white_elo:,} |
| Missing Black Elo | {missing_black_elo:,} |
| Missing Dates | {missing_dates:,} |

---

## Elo Coverage

| Metric | Value |
|----------|----------|
| White Elo Available | {white_elo_pct:.2f}% |
| Black Elo Available | {black_elo_pct:.2f}% |

---

## Elo Validation

| Check | Count |
|----------|----------|
| White Elo <1000 or >3500 | {invalid_white_elo:,} |
| Black Elo <1000 or >3500 | {invalid_black_elo:,} |

---

## Date Validation

| Check | Count |
|----------|----------|
| Future Dates | {future_dates:,} |

---

## Result Validation

| Check | Count |
|----------|----------|
| Invalid Results | {invalid_results:,} |

---

## Duplicate Validation

| Check | Count |
|----------|----------|
| Duplicate Game IDs | {duplicate_game_ids:,} |
"""

    report_path = (
        REPORTS_DIR
        / "data_quality.md"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(report)

    print(
        f"\nReport saved:\n{report_path}"
    )


def main():
    build_data_quality_report()


if __name__ == "__main__":
    main()