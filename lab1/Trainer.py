# Trainer.py
from User import User
from Fitness_program import  ProgramsManager
from Heart_rate_monitoring import Heart_rate_monitor
from Video_lessons import Video_lessons
from storage import load_json, save_json


class Trainer:
    """Главный класс фитнес-тренера."""

    def __init__(self):
        self.user = User("Александр", "Вашкевич", "похудение")
        self._load_user()
        self.programs_manager = ProgramsManager()
        self.video_lessons = Video_lessons()
        self.heart_monitor = Heart_rate_monitor()

    def _load_user(self):
        """Загружает пользователя из profile.json."""
        try:
            data = load_json("profile.json")
            self.user.name = data.get("имя пользователя", self.user.name)
            self.user.workouts_count = data.get("пройдено тренеровок", 0)
            self.user.rating = data.get("рейтинг", 0)
            self.user.current_program = data.get("текущая программа", None)
            self.user.completed_programs = data.get("завершённые программы", [])
            self.user.schedule = data.get("расписание", [])
        except Exception:
            pass

    def save_user(self):
        """Сохраняет пользователя в profile.json."""
        data = {
            "имя пользователя": self.user.name,
            "пройдено тренеровок": self.user.workouts_count,
            "рейтинг": self.user.rating,
            "текущая программа": self.user.current_program,
            "завершённые программы": self.user.completed_programs,
            "расписание": self.user.schedule
        }
        save_json(data, "profile.json")

    def add_workout(self):
        """Добавляет пройденную тренировку."""
        self.user.workouts_count += 1
        self.user.rating += 5
        self.save_user()

    def set_current_program(self, program_name: str):
        """Устанавливает текущую программу."""
        self.user.current_program = program_name
        self.save_user()

    def complete_current_program(self):
        """Завершает текущую программу."""
        if self.user.complete_current_program():
            self.save_user()
            return True
        return False

    def get_recommended_program(self):
        """Возвращает рекомендуемую программу (по рейтингу)."""
        return self.programs_manager.get_recommended_program()

    def get_programs_by_level(self, level: str):
        """Получает программы по уровню."""
        return self.programs_manager.get_programs_by_level(level)

    def get_programs_by_rating(self, min_rating: float):
        """Получает программы по рейтингу."""
        return self.programs_manager.get_programs_by_rating(min_rating)

    def rate_program(self, program_name: str, rating: float):
        """Оценивает программу."""
        self.programs_manager.rate_program(program_name, rating)

    def get_video_lessons_by_level(self, level: str):
        """Возвращает список видео для уровня (title, url)."""
        self.video_lessons.load_videos()
        if level == "начинающий":
            return self.video_lessons.beginner_videos
        elif level == "средний":
            return self.video_lessons.intermediate_videos
        elif level == "продвинутый":
            return self.video_lessons.advanced_videos
        return []

    def get_heart_monitor(self):
        return self.heart_monitor

    def get_user(self):
        return self.user