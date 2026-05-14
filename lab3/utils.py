import json
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
GAME_CONFIG_PATH = CONFIG_DIR / "game_config.json"
LEVELS_PATH = CONFIG_DIR / "levels.json"
RECORDS_PATH = DATA_DIR / "records.json"


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
