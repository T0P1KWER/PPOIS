# User.py


class User:
    """Класс пользователя."""

    def __init__(self, name: str = "Пользователь", lastname: str = "", training_goal: str = ""):
        self.name = name
        self.lastname = lastname
        self.training_goal = training_goal
        self.current_program = None
        self.completed_programs = []
        self.workouts_count = 0
        self.rating = 0
        self.schedule = []

    def add_workout(self):
        """Увеличивает счётчик тренировок."""
        self.workouts_count += 1
        self.rating += 5

    def set_program(self, program_name: str):
        """Устанавливает текущую программу."""
        self.current_program = program_name

    def complete_current_program(self):
        """Завершает текущую программу."""
        if self.current_program:
            self.completed_programs.append(self.current_program)
            self.current_program = None
            return True
        return False

    def show_profile(self):
        """Показывает профиль пользователя."""
        print("\n" + "=" * 50)
        print(f"        ПРОФИЛЬ: {self.name}")
        print("=" * 50)
        print(f"Текущая программа: {self.current_program if self.current_program else 'нет'}")
        print(f"Пройдено тренировок: {self.workouts_count}")
        print(f"Рейтинг: {self.rating}")
        print(f"\nЗавершённые программы: {len(self.completed_programs)}")
        if self.completed_programs:
            for i, prog in enumerate(self.completed_programs, 1):
                print(f"  {i}. {prog}")
        print(f"\nРасписание: {self._format_schedule()}")
        print("=" * 50)

    def _format_schedule(self) -> str:
        """Форматирует расписание для вывода."""
        days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        if not self.schedule:
            return "нет"
        return ", ".join([days[i - 1] for i in self.schedule])