from pathlib import Path

RAW_DIR = Path("data/raw")

EXPECTED_NAMES = {
    "caracteristiques": "caracteristiques.csv",
    "carcteristiques": "caracteristiques.csv",
    "caract": "caracteristiques.csv",
    "vehicules": "vehicules.csv",
    "usagers": "usagers.csv",
    "lieux": "lieux.csv",
}


def detect_type(filename: str) -> str | None:
    """
    Detect the BAAC file type from its filename.
    """
    name = filename.lower()

    for prefix, target_name in EXPECTED_NAMES.items():
        if name.startswith(prefix):
            return target_name

    return None


def rename_files():
    for year_dir in sorted(RAW_DIR.iterdir()):
        if not year_dir.is_dir():
            continue

        print(f"\n--- {year_dir.name} ---")

        for file_path in year_dir.glob("*.csv"):
            new_name = detect_type(file_path.name)

            if new_name is None:
                print(f"Ignoré : {file_path.name}")
                continue

            new_path = year_dir / new_name

            if file_path == new_path:
                print(f"Déjà correct : {file_path.name}")
                continue

            if new_path.exists():
                print(
                    f"ATTENTION : impossible de renommer "
                    f"{file_path.name} -> {new_name}, "
                    f"car {new_name} existe déjà."
                )
                continue

            file_path.rename(new_path)
            print(f"{file_path.name} -> {new_name}")


if __name__ == "__main__":
    rename_files()