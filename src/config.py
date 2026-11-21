from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

DB_PATH = PROCESSED / "chess.duckdb"

RESULT_MAP = {
    "0-1": 0,
    "1/2-1/2": 1,
    "1-0": 2
}