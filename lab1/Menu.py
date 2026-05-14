from Trainer import Trainer


class Menu:

    def __init__(self):
        self.trainer = Trainer()

    def show_main_menu(self):
        while True:
            print("\n" + "=" * 50)
            print("    ЭЛЕКТРОННЫЙ ФИТНЕС-ТРЕНЕР")
            print("=" * 50)
            print("1. Профиль")
            print("2. Программы")
            print("3. Видеоуроки")
            print("4. Показатели здоровья")
            print("5. Расписание тренировок")
            print("6. Выход")
            print("=" * 50)
            choice = input("Ваш выбор (1-6): ").strip()

            if choice == "1":
                self.show_profile()
            elif choice == "2":
                self.show_programs_menu()
            elif choice == "3":
                self.show_video_menu()
            elif choice == "4":
                self.show_heart_menu()
            elif choice == "5":
                self.show_schedule_menu()
            elif choice == "6":
                print("\n До свидания!")
                break
            else:
                print("\n Неизвестный выбор")

    def show_profile(self):
        user = self.trainer.get_user()
        print("\n" + "=" * 50)
        print(f"        ПРОФИЛЬ: {user.name}")
        print("=" * 50)
        print(f"Текущая программа: {user.current_program if user.current_program else 'нет'}")
        print(f"Пройдено тренировок: {user.workouts_count}")
        print(f"Рейтинг: {user.rating}")
        print(f"\nЗавершённые программы: {len(user.completed_programs)}")
        if user.completed_programs:
            for i, prog in enumerate(user.completed_programs, 1):
                print(f"  {i}. {prog}")
        print(f"\nРасписание: {user._format_schedule()}")
        print("=" * 50)
        input("\nНажмите Enter...")

    def show_programs_menu(self):
        while True:
            print("\n" + "-" * 50)
            print("        ПРОГРАММЫ ТРЕНИРОВОК")
            print("-" * 50)
            print("1. Выбрать программу")
            print("2. Рекомендованная программа")
            print("3. Завершить текущую программу")
            print("4. Назад")
            print("-" * 50)

            choice = input("Ваш выбор (1-4): ").strip()

            if choice == "1":
                self._select_program()
            elif choice == "2":
                self._show_recommended_program()
            elif choice == "3":
                self._complete_current_program()
            elif choice == "4":
                break
            else:
                print("\n Неверный выбор")

    def _select_program(self):
        programs = self.trainer.programs_manager.get_all_programs()
        if not programs:
            print("\n Нет доступных программ")
            input("\nНажмите Enter...")
            return

        print("\nДоступные программы:")
        print("-" * 50)
        for i, program in enumerate(programs, 1):
            print(f"{i}. {program.name} ({program.level}, {program.duration} мин)")
        print("-" * 50)

        try:
            prog_choice = input(f"\nВыберите программу (1-{len(programs)}): ").strip()
            index = int(prog_choice) - 1
            if 0 <= index < len(programs):
                selected = programs[index]
                self.trainer.set_current_program(selected.name)
                print(f"\n Программа '{selected.name}' установлена!")
            else:
                print("\n Неверный номер")
        except ValueError:
            print("\n Введите число")
        input("\nНажмите Enter...")

    def _show_recommended_program(self):
        program = self.trainer.get_recommended_program()
        if program:
            print(f"\n Рекомендуемая программа:")
            print("-" * 50)
            print(program.get_info())
            print("-" * 50)

            set_choice = input("\nУстановить эту программу? (да/нет): ").strip().lower()
            if set_choice == "да":
                self.trainer.set_current_program(program.name)
                print(f"\n Программа '{program.name}' установлена!")
        else:
            print("\n Нет доступных программ")
        input("\nНажмите Enter...")

    def _complete_current_program(self):
        user = self.trainer.get_user()

        if not user.current_program:
            print("\n️ Нет активной программы для завершения")
            input("\nНажмите Enter...")
            return

        program_name = user.current_program
        print(f"\nТекущая программа: {program_name}")
        confirm = input("Завершить эту программу? (да/нет): ").strip().lower()

        if confirm == "да":
            if self.trainer.complete_current_program():
                # ← ИСПРАВЛЕНО: используем сохранённое имя
                print(f"\n Программа '{program_name}' завершена!")
                print(" Поздравляем с завершением!")
            else:
                print("\n Ошибка при завершении программы")
        else:
            print("\n Завершение отменено")

        input("\nНажмите Enter...")

    def show_video_menu(self):
        while True:
            print("\n" + "-" * 50)
            print("        ВЫБЕРИТЕ УРОВЕНЬ СЛОЖНОСТИ")
            print("-" * 50)
            print("1. Начинающий")
            print("2. Средний")
            print("3. Продвинутый")
            print("4. Назад")
            print("-" * 50)

            choice = input("Ваш выбор (1-4): ").strip()

            if choice == "1":
                self._show_and_complete_videos("начинающий")
            elif choice == "2":
                self._show_and_complete_videos("средний")
            elif choice == "3":
                self._show_and_complete_videos("продвинутый")
            elif choice == "4":
                break
            else:
                print("\n Неверный выбор")

    def _show_and_complete_videos(self, level: str):
        videos = self.trainer.get_video_lessons_by_level(level)
        if not videos:
            print(f"\n Нет видео для уровня '{level}'")
            input("\nНажмите Enter...")
            return

        while True:
            print(f"\nВидео для уровня '{level}':")
            print("-" * 50)

            for i, (title, url) in enumerate(videos, 1):
                print(f"{i}. {title}")

            print("0. Назад")
            print("-" * 50)

            choice = input(f"Выберите (0-{len(videos)}): ").strip()

            if choice == "0":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(videos):
                    title, url = videos[idx]
                    print(f"\n🎬 {title}")
                    print(f"Ссылка: {url}")
                    input("\nНажмите Enter, чтобы засчитать тренировку...")
                    self.trainer.add_workout()
                    print("\n Тренировка засчитана!")
                else:
                    print("\n Номер вне диапазона")
            except ValueError:
                print("\n Введите число")

    def show_heart_menu(self):
        monitor = self.trainer.get_heart_monitor()
        while True:
            print("\n" + "-" * 50)
            print("        ПУЛЬСОМЕТР")
            print("-" * 50)
            print("1. Замерить пульс")
            print("2. Проверить статус")
            print("3. Назад")
            print("-" * 50)

            choice = input("Ваш выбор (1-3): ").strip()

            if choice == "1":
                monitor.set_heart_rate()
            elif choice == "2":
                status = monitor.get_heart_rate_status()
                print("\n" + "=" * 50)
                print(status)
                print("=" * 50)
                input("\nНажмите Enter...")
            elif choice == "3":
                break
            else:
                print("\n Неверный выбор")

    def show_schedule_menu(self):
        user = self.trainer.get_user()
        days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]

        print("\n" + "=" * 50)
        print("        РАСПИСАНИЕ ТРЕНИРОВОК")
        print("=" * 50)

        current = ", ".join([days[i - 1] for i in user.schedule]) if user.schedule else "нет"
        print(f"Текущее расписание: {current}")

        print("\nВведите дни недели (1-7) через запятую:")
        print("1=понедельник, 2=вторник, 3=среда, 4=четверг, 5=пятница, 6=суббота, 7=воскресенье")

        new_days = input("\nВаш выбор: ").strip()
        if new_days:
            try:
                user.schedule = [
                    int(day) for day in new_days.split(",")
                    if day.strip().isdigit() and 1 <= int(day.strip()) <= 7
                ]
                self.trainer.save_user()
                print("\n Расписание обновлено!")
            except:
                print("\n Некорректный ввод. Пример: 1,3,5")

        input("\nНажмите Enter...")