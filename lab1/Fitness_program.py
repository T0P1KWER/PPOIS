
from storage import load_json, save_json


class Fitness_program:

    def __init__(self, name: str, level: str, duration: int, exercises: list, rating: float = 0.0):
        self.name = name
        self.level = level
        self.duration = duration
        self.exercises = exercises
        self.rating = rating
        self.completed = False

    def mark_as_completed(self):

        self.completed = True

    def __str__(self):
        exercises_list = ", ".join(self.exercises)
        status = "Завершена" if self.completed else "В процессе"
        return f"Программа: {self.name}\nУровень: {self.level}\nДлительность: {self.duration} мин\nУпражнения: {exercises_list}\nСтатус: {status}"

    def get_info(self) -> str:
        """Краткая информация о программе."""
        status = " Завершена" if self.completed else " В процессе"
        return f"{self.name} | Уровень: {self.level} | {self.duration} мин | Рейтинг: {self.rating}/5.0 | {status}"


class ProgramsManager:


    def __init__(self, filename: str = "programs.json"):
        self.filename = filename
        self.programs = self.load_programs()

    def load_programs(self) -> list:

        try:
            data = load_json(self.filename)

            programs = []
            for item in data:
                programs.append(Fitness_program(
                    name=item["name"],
                    level=item["level"],
                    duration=item["duration"],
                    exercises=item["exercises"],
                    rating=item.get("rating", 0.0)
                ))
            return programs

        except FileNotFoundError:
            print(f"⚠️ Файл {self.filename} не найден. Создаём примеры...")
            return self.create_default_programs()

    def create_default_programs(self) -> list:

        return [
            Fitness_program(
                name="Кардио для начинающих",
                level="начинающий",
                duration=30,
                exercises=["Бег на месте", "Приседания", "Отжимания"],
                rating=4.5
            ),
            Fitness_program(
                name="Силовая тренировка",
                level="средний",
                duration=45,
                exercises=["Жим лёжа", "Приседания со штангой", "Тяга"],
                rating=4.7
            ),
            Fitness_program(
                name="HIIT тренировка",
                level="продвинутый",
                duration=20,
                exercises=["Бёрпи", "Прыжки", "Планка"],
                rating=4.3
            )
        ]

    def save_programs(self):

        data = []
        for program in self.programs:
            data.append({
                "name": program.name,
                "level": program.level,
                "duration": program.duration,
                "exercises": program.exercises,
                "rating": program.rating
            })

        save_json(data, self.filename)

    def get_all_programs(self) -> list:

        return self.programs

    def get_programs_by_level(self, level: str) -> list:

        return [prog for prog in self.programs if prog.level == level]

    def get_programs_by_rating(self, min_rating: float) -> list:

        return [prog for prog in self.programs if prog.rating >= min_rating]

    def get_recommended_program(self):

        if not self.programs:
            return None
        return max(self.programs, key=lambda x: x.rating)

    def add_program(self, program: Fitness_program):

        self.programs.append(program)
        self.save_programs()

    def rate_program(self, program_name: str, rating: float):

        for program in self.programs:
            if program.name == program_name:
                program.rating = (program.rating + rating) / 2
                self.save_programs()
                print(f"\n Программа '{program_name}' оценена {rating}/5.0")
                return
        print("\n Программа не найдена")