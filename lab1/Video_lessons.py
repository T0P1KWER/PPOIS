
import json


class Video_lessons:


    def __init__(self):
        self.beginner_videos = []
        self.intermediate_videos = []
        self.advanced_videos = []

    def load_videos(self):
        try:
            with open("videos.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            self.beginner_videos = [
                (item["title"], item["url"])
                for item in data["начинающий"]
            ]

            self.intermediate_videos = [
                (item["title"], item["url"])
                for item in data["средний"]
            ]

            self.advanced_videos = [
                (item["title"], item["url"])
                for item in data["продвинутый"]
            ]
        except FileNotFoundError:
            print(" Файл videos.json не найден. Создайте файл с видеоуроками.")

    def show_beginner_videos(self):

        self.load_videos()

        if not self.beginner_videos:
            print("\n Нет видео для начинающих")
            return False

        while True:
            print("\n" + "=" * 50)
            print("        ВИДЕО ДЛЯ НАЧИНАЮЩИХ")
            print("=" * 50)

            for i, (title, url) in enumerate(self.beginner_videos, 1):
                print(f"{i}. {title}")

            print("0. Назад")
            print("=" * 50)

            choice = input(f"Выберите видео (0-{len(self.beginner_videos)}): ").strip()

            if choice == "0":
                return False

            try:
                index = int(choice) - 1
                if 0 <= index < len(self.beginner_videos):
                    title, url = self.beginner_videos[index]
                    print(f"\n🎬 Воспроизведение: {title}")
                    print(f"Ссылка: {url}")
                    input("\nНажмите Enter, чтобы отметить урок пройденным...")
                    return True
                else:
                    print(f"\n Неверный номер.")
            except ValueError:
                print("\n Введите число.")

    def show_intermediate_videos(self):

        self.load_videos()

        if not self.intermediate_videos:
            print("\n️ Нет видео для среднего уровня")
            return False

        while True:
            print("\n" + "=" * 50)
            print("        ВИДЕО ДЛЯ СРЕДНЕГО УРОВНЯ")
            print("=" * 50)

            for i, (title, url) in enumerate(self.intermediate_videos, 1):
                print(f"{i}. {title}")

            print("0. Назад")
            print("=" * 50)

            choice = input(f"Выберите видео (0-{len(self.intermediate_videos)}): ").strip()

            if choice == "0":
                return False

            try:
                index = int(choice) - 1
                if 0 <= index < len(self.intermediate_videos):
                    title, url = self.intermediate_videos[index]
                    print(f"\n🎬 Воспроизведение: {title}")
                    print(f"Ссылка: {url}")
                    input("\nНажмите Enter, чтобы отметить урок пройденным...")
                    return True
                else:
                    print(f"\n Неверный номер.")
            except ValueError:
                print("\nВведите число.")

    def show_advanced_videos(self):
        self.load_videos()

        if not self.advanced_videos:
            print("\n Нет видео для продвинутого уровня")
            return False

        while True:
            print("\n" + "=" * 50)
            print("        ВИДЕО ДЛЯ ПРОДВИНУТЫХ")
            print("=" * 50)

            for i, (title, url) in enumerate(self.advanced_videos, 1):
                print(f"{i}. {title}")

            print("0. Назад")
            print("=" * 50)

            choice = input(f"Выберите видео (0-{len(self.advanced_videos)}): ").strip()

            if choice == "0":
                return False

            try:
                index = int(choice) - 1
                if 0 <= index < len(self.advanced_videos):
                    title, url = self.advanced_videos[index]
                    print(f"\n🎬 Воспроизведение: {title}")  # ← ИСПРАВЛЕНО: добавлена скобка после print
                    print(f"Ссылка: {url}")
                    input("\nНажмите Enter, чтобы отметить урок пройденным...")
                    return True
                else:
                    print(f"\n Неверный номер.")
            except ValueError:
                print("\n Введите число.")