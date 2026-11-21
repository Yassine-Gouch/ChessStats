from pathlib import Path
import requests
import zipfile
import time
from tqdm import tqdm


RAW = Path("data/raw")

HEADERS = {
    "User-Agent": "chess-stats-project"
}


def download(url: str, dest: Path, retries: int = 3) -> Path:
    """
    Download a file with retries.
    Skip if already exists.
    """

    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists():
        print(f"SKIP: {dest.name} already exists")
        return dest

    for attempt in range(1, retries + 1):

        try:

            print(f"Downloading: {url}")

            with requests.get(
                url,
                stream=True,
                headers=HEADERS,
                timeout=60
            ) as response:

                response.raise_for_status()

                total = int(
                    response.headers.get("content-length", 0)
                )

                with open(dest, "wb") as f, tqdm(
                    total=total,
                    unit="B",
                    unit_scale=True,
                    desc=dest.name
                ) as bar:

                    for chunk in response.iter_content(
                        chunk_size=1024 * 1024
                    ):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))

            return dest

        except Exception as e:

            print(
                f"Attempt {attempt}/{retries} failed: {e}"
            )

            if attempt == retries:
                raise

            time.sleep(3)

    return dest


def unzip(zip_path: Path, output_dir: Path) -> None:
    """
    Extract zip file.
    """

    try:

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(output_dir)

    except Exception as e:

        print(f"Unzip error: {zip_path}")
        print(e)


def twic_range(first: int, last: int) -> None:
    """
    Download TWIC issues.
    Example:
    twic_range(1600, 1667)
    """

    twic_dir = RAW / "twic"

    for issue in range(first, last + 1):

        try:

            zip_name = f"twic{issue}g.zip"

            url = (
                f"https://theweekinchess.com/zips/{zip_name}"
            )

            zip_path = twic_dir / zip_name

            download(url, zip_path)

            unzip(zip_path, twic_dir)

            print(f"OK: TWIC {issue}")

        except Exception as e:

            print(f"FAILED TWIC {issue}: {e}")

        time.sleep(1)


def pgnmentor(players=None):
    """
    Download PGN Mentor player files.
    """

    if players is None:

        players = [
            "Carlsen",
            "Nakamura",
            "Caruana",
            "Kasparov",
            "Fischer"
        ]

    output = RAW / "pgnmentor"

    for player in players:

        try:

            url = (
                f"https://www.pgnmentor.com/players/{player}.zip"
            )

            zip_path = output / f"{player}.zip"

            download(url, zip_path)

            unzip(zip_path, output)

        except Exception as e:

            print(f"SKIP {player}: {e}")

        time.sleep(1)


def fide():
    """
    Manual download message.
    """

    fide_dir = RAW / "fide"

    xml_files = list(fide_dir.glob("*.xml"))

    if xml_files:

        print(
            f"FIDE OK: {len(xml_files)} XML file(s) found"
        )

        return

    print("\nFIDE XML not found.\n")
    print(
        "Download manually from:"
    )
    print(
        "https://ratings.fide.com/download_lists.phtml"
    )
    print(
        "Place XML files inside:"
    )
    print(
        "data/raw/fide/"
    )


if __name__ == "__main__":

    fide()

    # Small test
    # twic_range(1663, 1667)

    # Recommended first batch
    twic_range(1600, 1667)

    # Optional later
    # pgnmentor()