from datetime import datetime

import pygame

from audio_manager import AudioManager
from board import Board
from button import Button
from utils import GAME_CONFIG_PATH, LEVELS_PATH, RECORDS_PATH, load_json, save_json


class JewelQuestApp:
    def __init__(self):
        pygame.init()

        self.config = load_json(GAME_CONFIG_PATH)
        self.levels = load_json(LEVELS_PATH)
        self.records = load_json(RECORDS_PATH)

        window = self.config["window"]
        self.screen = pygame.display.set_mode((window["width"], window["height"]))
        pygame.display.set_caption(self.config["window"]["title"])
        self.clock = pygame.time.Clock()

        self.colors = {name: tuple(value) for name, value in self.config["colors"].items()}
        self.fonts = {
            "title": pygame.font.SysFont("arial", 44, bold=True),
            "subtitle": pygame.font.SysFont("arial", 28, bold=True),
            "text": pygame.font.SysFont("arial", 24),
            "small": pygame.font.SysFont("arial", 18),
            "button": pygame.font.SysFont("arial", 26, bold=True),
        }

        audio_config = self.config["audio"]
        self.audio = AudioManager(
            enabled=audio_config["enabled"],
            volume_effects=audio_config["effects_volume"],
            volume_music=audio_config["music_volume"],
        )
        self.audio.play_music()

        self.board = Board(
            board_config=self.config["board"],
            gem_types=self.config["board"]["starting_gem_types"],
            tile_colors=self.config["tile_colors"],
        )

        self.running = True
        self.screen_state = "menu"

        self.current_mode = None
        self.current_level_index = 0
        self.current_level_data = None
        self.score = 0
        self.time_left = 0.0
        self.moves_left = 0
        self.target_score = 0
        self.last_result_text = ""
        self.last_result_score = 0
        self.shuffle_message_timer = 0.0

        self.awaiting_name = False
        self.player_name_input = ""

        self.menu_buttons = self._build_menu_buttons()
        self.mode_buttons = self._build_mode_buttons()
        self.back_button = Button((40, 650, 180, 52), "Назад", self.fonts["button"], (72, 84, 112), (94, 108, 142), (255, 255, 255))

    def _build_menu_buttons(self):
        return [
            Button((430, 240, 340, 64), "Начать игру", self.fonts["button"], (103, 162, 92), (124, 190, 112), (255, 255, 255)),
            Button((430, 324, 340, 64), "Таблица рекордов", self.fonts["button"], (72, 126, 176), (91, 149, 200), (255, 255, 255)),
            Button((430, 408, 340, 64), "Выход", self.fonts["button"], (157, 79, 79), (183, 94, 94), (255, 255, 255)),
        ]

    def _build_mode_buttons(self):
        return [
            Button((380, 260, 440, 68), "Режим на время", self.fonts["button"], (88, 142, 109), (106, 166, 126), (255, 255, 255)),
            Button((380, 352, 440, 68), "Режим по уровням", self.fonts["button"], (83, 117, 173), (102, 137, 199), (255, 255, 255)),
            Button((380, 444, 440, 68), "Вернуться в меню", self.fonts["button"], (108, 90, 128), (128, 108, 150), (255, 255, 255)),
        ]

    def reset_common_game_state(self):
        self.score = 0
        self.last_result_score = 0
        self.last_result_text = ""
        self.awaiting_name = False
        self.player_name_input = ""
        self.shuffle_message_timer = 0.0

    def start_timed_mode(self):
        self.reset_common_game_state()
        self.current_mode = "timed"
        self.time_left = self.config["modes"]["timed"]["seconds"]
        self.moves_left = 0
        self.target_score = 0
        self.current_level_index = 0
        self.current_level_data = None
        self.board.reset_with_gem_count(self.config["board"]["starting_gem_types"])
        self.screen_state = "game"

    def start_level_mode(self):
        self.reset_common_game_state()
        self.current_mode = "levels"
        self.current_level_index = 0
        self.load_level(self.current_level_index)
        self.screen_state = "game"

    def load_level(self, level_index):
        self.current_level_data = self.levels[level_index]
        self.moves_left = self.current_level_data["moves"]
        self.target_score = self.current_level_data["target_score"]
        self.board.reset_with_gem_count(self.current_level_data["gem_types"])

    def finish_game(self, result_text):
        self.last_result_text = result_text
        self.last_result_score = self.score
        self.screen_state = "result"

        top_score = self.records[0]["score"] if self.records else -1
        self.awaiting_name = self.score > top_score
        self.player_name_input = ""

        if "поздрав" in result_text.lower() or "пройдены" in result_text.lower():
            self.audio.play("win")
        else:
            self.audio.play("lose")

    def save_record(self):
        player_name = self.player_name_input.strip() or "Игрок"
        mode_name = "На время" if self.current_mode == "timed" else "По уровням"

        self.records.append(
            {
                "name": player_name[:16],
                "score": self.score,
                "mode": mode_name,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )

        self.records.sort(key=lambda item: item["score"], reverse=True)
        self.records = self.records[:10]
        save_json(RECORDS_PATH, self.records)
        self.awaiting_name = False

    def draw_background(self):
        self.screen.fill(self.colors["background"])

        for index in range(7):
            top = index * 110
            pygame.draw.rect(self.screen, self.colors["panel_soft"], (0, top, 1200, 55))

    def draw_title(self, subtitle=None):
        title_surface = self.fonts["title"].render("Jewel Quest: Вариант 8", True, self.colors["title"])
        title_rect = title_surface.get_rect(center=(600, 90))
        self.screen.blit(title_surface, title_rect)

        if subtitle:
            subtitle_surface = self.fonts["subtitle"].render(subtitle, True, self.colors["text_light"])
            subtitle_rect = subtitle_surface.get_rect(center=(600, 135))
            self.screen.blit(subtitle_surface, subtitle_rect)

    def draw_menu(self):
        self.draw_background()


        lines = [
        ]

        for index, line in enumerate(lines):
            surface = self.fonts["text"].render(line, True, self.colors["text"])
            rect = surface.get_rect(center=(600, 170 + index * 28))
            self.screen.blit(surface, rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            button.draw(self.screen, mouse_pos)

    def draw_mode_select(self):
        self.draw_background()
        self.draw_title("Выбор режима")

        lines = []

        for index, line in enumerate(lines):
            surface = self.fonts["text"].render(line, True, self.colors["text"])
            rect = surface.get_rect(center=(600, 190 + index * 34))
            self.screen.blit(surface, rect)


        mouse_pos = pygame.mouse.get_pos()
        for button in self.mode_buttons:
            button.draw(self.screen, mouse_pos)

    def draw_records(self):
        self.draw_background()
        self.draw_title("Таблица рекордов")

        panel = pygame.Rect(160, 180, 880, 420)
        pygame.draw.rect(self.screen, self.colors["panel"], panel, border_radius=18)
        pygame.draw.rect(self.screen, self.colors["panel_border"], panel, width=2, border_radius=18)

        headers = [("Место", 200), ("Имя", 320), ("Очки", 540), ("Режим", 690), ("Дата", 860)]
        for title, x in headers:
            surface = self.fonts["subtitle"].render(title, True, self.colors["title"])
            rect = surface.get_rect(center=(x, 220))
            self.screen.blit(surface, rect)

        if not self.records:
            empty_text = self.fonts["text"].render("Пока рекордов нет. Сыграй первую партию.", True, self.colors["text"])
            self.screen.blit(empty_text, empty_text.get_rect(center=(600, 380)))
        else:
            for index, record in enumerate(self.records[:10]):
                row_y = 275 + index * 30
                values = [
                    (str(index + 1), 200),
                    (record["name"], 320),
                    (str(record["score"]), 540),
                    (record["mode"], 690),
                    (record["date"], 860),
                ]

                for text, x in values:
                    surface = self.fonts["small"].render(text, True, self.colors["text"])
                    rect = surface.get_rect(center=(x, row_y))
                    self.screen.blit(surface, rect)

        self.back_button.draw(self.screen, pygame.mouse.get_pos())

    def draw_game(self):
        self.draw_background()

        subtitle = "Режим на время" if self.current_mode == "timed" else f"Уровень {self.current_level_index + 1}"
        self.draw_title(subtitle)

        panel = pygame.Rect(720, 200, 360, 370)
        pygame.draw.rect(self.screen, self.colors["panel"], panel, border_radius=18)
        pygame.draw.rect(self.screen, self.colors["panel_border"], panel, width=2, border_radius=18)

        self.board.draw(self.screen)

        info_lines = [f"Очки: {self.score}"]

        if self.current_mode == "timed":
            info_lines.append(f"Осталось времени: {max(0, int(self.time_left))} сек.")
            info_lines.append("Цель: набрать как можно больше очков")
        else:
            info_lines.append(f"Цель уровня: {self.target_score} очков")
            info_lines.append(f"Осталось ходов: {self.moves_left}")
            info_lines.append(f"Типов камней: {self.current_level_data['gem_types']}")

        if self.shuffle_message_timer > 0:
            info_lines.append("Поле перемешано: возможных ходов не было")

        for index, line in enumerate(info_lines):
            surface = self.fonts["text"].render(line, True, self.colors["text"])
            self.screen.blit(surface, (750, 245 + index * 42))

        tip_lines = [
            "Управление:",
            "ЛКМ по камню -> выбрать",
            "ЛКМ по соседнему -> обменять",
            "ESC -> вернуться в меню",
        ]

        for index, line in enumerate(tip_lines):
            surface = self.fonts["small"].render(line, True, self.colors["text_light"])
            self.screen.blit(surface, (750, 430 + index * 28))

    def draw_result(self):
        self.draw_background()
        self.draw_title("Результат партии")

        panel = pygame.Rect(260, 200, 680, 320)
        pygame.draw.rect(self.screen, self.colors["panel"], panel, border_radius=18)
        pygame.draw.rect(self.screen, self.colors["panel_border"], panel, width=2, border_radius=18)

        result_surface = self.fonts["subtitle"].render(self.last_result_text, True, self.colors["title"])
        score_surface = self.fonts["text"].render(f"Финальный счёт: {self.last_result_score}", True, self.colors["text"])
        self.screen.blit(result_surface, result_surface.get_rect(center=(600, 260)))
        self.screen.blit(score_surface, score_surface.get_rect(center=(600, 315)))

        if self.awaiting_name:
            prompt = self.fonts["text"].render("Новый рекорд. Введи имя и нажми Enter:", True, self.colors["text"])
            self.screen.blit(prompt, prompt.get_rect(center=(600, 370)))

            input_rect = pygame.Rect(410, 405, 380, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), input_rect, border_radius=10)
            pygame.draw.rect(self.screen, self.colors["panel_border"], input_rect, width=2, border_radius=10)

            input_surface = self.fonts["text"].render(self.player_name_input or "Игрок", True, (40, 40, 40))
            self.screen.blit(input_surface, (425, 416))

            hint = self.fonts["small"].render("Backspace удаляет символ, Enter сохраняет результат.", True, self.colors["text_light"])
            self.screen.blit(hint, hint.get_rect(center=(600, 480)))
        else:
            prompt = self.fonts["text"].render("Нажми Enter, чтобы вернуться в меню.", True, self.colors["text"])
            self.screen.blit(prompt, prompt.get_rect(center=(600, 395)))

    def update_game(self, dt):
        board_events = self.board.update(dt)
        self.score += board_events["score_delta"]

        if board_events["score_delta"] > 0:
            self.audio.play("match")

        if board_events["move_completed"]:
            self.audio.play("drop")
            if self.current_mode == "levels":
                self.moves_left -= 1

        if board_events["shuffle_happened"]:
            self.shuffle_message_timer = 2.0

        if self.shuffle_message_timer > 0:
            self.shuffle_message_timer -= dt

        if self.current_mode == "timed":
            self.time_left -= dt
            if self.time_left <= 0:
                self.finish_game("Время вышло")
        else:
            if self.score >= self.target_score:
                if self.current_level_index + 1 < len(self.levels):
                    self.current_level_index += 1
                    self.load_level(self.current_level_index)
                else:
                    self.finish_game("Поздравляем, все уровни пройдены")
            elif self.moves_left <= 0 and not self.board.is_busy():
                self.finish_game("Ходы закончились")

    def handle_menu_events(self, event):
        if self.menu_buttons[0].is_clicked(event):
            self.screen_state = "mode_select"
        elif self.menu_buttons[1].is_clicked(event):
            self.screen_state = "records"
        elif self.menu_buttons[2].is_clicked(event):
            self.running = False

    def handle_mode_select_events(self, event):
        if self.mode_buttons[0].is_clicked(event):
            self.start_timed_mode()
        elif self.mode_buttons[1].is_clicked(event):
            self.start_level_mode()
        elif self.mode_buttons[2].is_clicked(event):
            self.screen_state = "menu"

    def handle_records_events(self, event):
        if self.back_button.is_clicked(event):
            self.screen_state = "menu"

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.screen_state = "menu"
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell = self.board.get_cell_from_mouse(event.pos)
            if cell is None:
                return

            action = self.board.handle_click(cell)
            if action == "select":
                self.audio.play("select")
            elif action == "swap":
                self.audio.play("swap")

    def handle_result_events(self, event):
        if self.awaiting_name:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.save_record()
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name_input = self.player_name_input[:-1]
                else:
                    if event.unicode.isprintable() and len(self.player_name_input) < 16:
                        self.player_name_input += event.unicode
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.screen_state = "menu"

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.screen_state == "menu":
                    self.handle_menu_events(event)
                elif self.screen_state == "mode_select":
                    self.handle_mode_select_events(event)
                elif self.screen_state == "records":
                    self.handle_records_events(event)
                elif self.screen_state == "game":
                    self.handle_game_events(event)
                elif self.screen_state == "result":
                    self.handle_result_events(event)

            if self.screen_state == "game":
                self.update_game(dt)

            if self.screen_state == "menu":
                self.draw_menu()
            elif self.screen_state == "mode_select":
                self.draw_mode_select()
            elif self.screen_state == "records":
                self.draw_records()
            elif self.screen_state == "game":
                self.draw_game()
            elif self.screen_state == "result":
                self.draw_result()

            pygame.display.flip()

        self.audio.stop_music()
        pygame.quit()
