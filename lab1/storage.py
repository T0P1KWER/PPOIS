# storage.py
import json


def load_json(filename: str) -> dict:
    """Загружает JSON из файла."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка в формате JSON файла '{filename}': {e}")


def save_json(data: dict, filename: str):
    """Сохраняет данные в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_field(filename: str, key: str, value):
    """Обновляет одно поле в JSON-файле."""
    data = load_json(filename)
    data[key] = value
    save_json(data, filename)