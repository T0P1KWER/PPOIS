import random

import pygame


class Board:
    def __init__(self, board_config, gem_types, tile_colors):
        self.rows = board_config["rows"]
        self.cols = board_config["cols"]
        self.tile_size = board_config["tile_size"]
        self.x = board_config["offset_x"]
        self.y = board_config["offset_y"]
        self.background_color = tuple(board_config["background_color"])
        self.frame_color = tuple(board_config["frame_color"])
        self.cell_color = tuple(board_config["cell_color"])

        self.available_gem_types = gem_types
        self.tile_colors = {int(key): tuple(value) for key, value in tile_colors.items()}

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.selected_cell = None

        self.swap_animation = None
        self.remove_animation = None
        self.fall_animation = None

        self.current_matches = set()
        self.score_to_add = 0
        self.completed_player_move = False

        self.fill_without_matches()

    def reset_with_gem_count(self, gem_count):
        self.available_gem_types = gem_count
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.selected_cell = None
        self.swap_animation = None
        self.remove_animation = None
        self.fall_animation = None
        self.current_matches = set()
        self.score_to_add = 0
        self.completed_player_move = False
        self.fill_without_matches()

    def fill_without_matches(self):
        for row in range(self.rows):
            for col in range(self.cols):
                choices = list(range(self.available_gem_types))

                if col >= 2 and self.grid[row][col - 1] == self.grid[row][col - 2]:
                    if self.grid[row][col - 1] in choices:
                        choices.remove(self.grid[row][col - 1])

                if row >= 2 and self.grid[row - 1][col] == self.grid[row - 2][col]:
                    if self.grid[row - 1][col] in choices:
                        choices.remove(self.grid[row - 1][col])

                self.grid[row][col] = random.choice(choices)

        if not self.has_possible_moves():
            self.shuffle_board()

    def shuffle_board(self):
        values = [self.grid[row][col] for row in range(self.rows) for col in range(self.cols)]

        while True:
            random.shuffle(values)
            index = 0

            for row in range(self.rows):
                for col in range(self.cols):
                    self.grid[row][col] = values[index]
                    index += 1

            if not self.find_matches() and self.has_possible_moves():
                break

    def get_cell_from_mouse(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos

        if mouse_x < self.x or mouse_y < self.y:
            return None

        col = (mouse_x - self.x) // self.tile_size
        row = (mouse_y - self.y) // self.tile_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col

        return None

    def is_busy(self):
        return self.swap_animation is not None or self.remove_animation is not None or self.fall_animation is not None

    def are_neighbors(self, first, second):
        row_1, col_1 = first
        row_2, col_2 = second
        return abs(row_1 - row_2) + abs(col_1 - col_2) == 1

    def swap_cells(self, first, second):
        row_1, col_1 = first
        row_2, col_2 = second
        self.grid[row_1][col_1], self.grid[row_2][col_2] = self.grid[row_2][col_2], self.grid[row_1][col_1]

    def handle_click(self, cell):
        if self.is_busy():
            return None

        if self.selected_cell is None:
            self.selected_cell = cell
            return "select"

        if cell == self.selected_cell:
            self.selected_cell = None
            return None

        if self.are_neighbors(self.selected_cell, cell):
            first = self.selected_cell
            second = cell
            self.selected_cell = None
            self.start_swap_animation(first, second, is_return=False)
            return "swap"

        self.selected_cell = cell
        return "select"

    def start_swap_animation(self, first, second, is_return):
        self.swap_cells(first, second)
        self.swap_animation = {
            "first": first,
            "second": second,
            "elapsed": 0.0,
            "duration": 0.18,
            "is_return": is_return,
            "first_value": self.grid[first[0]][first[1]],
            "second_value": self.grid[second[0]][second[1]],
        }

    def find_matches(self):
        matches = set()

        for row in range(self.rows):
            streak = 1
            for col in range(1, self.cols):
                current = self.grid[row][col]
                previous = self.grid[row][col - 1]


                if current is not None and current == previous:
                    streak += 1
                else:
                    if streak >= 3:
                        for offset in range(streak):
                            matches.add((row, col - 1 - offset))
                    streak = 1

            if streak >= 3:
                for offset in range(streak):
                    matches.add((row, self.cols - 1 - offset))

        for col in range(self.cols):
            streak = 1
            for row in range(1, self.rows):
                current = self.grid[row][col]
                previous = self.grid[row - 1][col]

                if current is not None and current == previous:
                    streak += 1
                else:
                    if streak >= 3:
                        for offset in range(streak):
                            matches.add((row - 1 - offset, col))
                    streak = 1

            if streak >= 3:
                for offset in range(streak):
                    matches.add((self.rows - 1 - offset, col))

        return matches

    def has_possible_moves(self):
        directions = [(0, 1), (1, 0)]

        for row in range(self.rows):
            for col in range(self.cols):
                for delta_row, delta_col in directions:
                    next_row = row + delta_row
                    next_col = col + delta_col

                    if next_row >= self.rows or next_col >= self.cols:
                        continue

                    self.swap_cells((row, col), (next_row, next_col))
                    matches_exist = bool(self.find_matches())
                    self.swap_cells((row, col), (next_row, next_col))

                    if matches_exist:
                        return True

        return False

    def start_remove_animation(self, matches, chain_multiplier):
        self.current_matches = matches
        self.score_to_add = len(matches) * 10 * chain_multiplier
        self.remove_animation = {
            "elapsed": 0.0,
            "duration": 0.22,
        }

    def build_fall_animation(self):
        moving_tiles = []

        for col in range(self.cols):
            old_column = [self.grid[row][col] for row in range(self.rows)]
            compacted = [value for value in old_column if value is not None]
            new_count = self.rows - len(compacted)
            new_values = [random.randrange(self.available_gem_types) for _ in range(new_count)]
            final_column = new_values + compacted

            source_rows = []

            for index in range(new_count):
                source_rows.append(index - new_count)

            for old_row, old_value in enumerate(old_column):
                if old_value is not None:
                    source_rows.append(old_row)

            for row in range(self.rows):
                value = final_column[row]
                start_row = source_rows[row]

                if start_row != row:
                    moving_tiles.append(
                        {
                            "value": value,
                            "col": col,
                            "start_row": start_row,
                            "end_row": row,
                        }
                    )

            for row in range(self.rows):
                self.grid[row][col] = final_column[row]

        self.fall_animation = {
            "elapsed": 0.0,
            "duration": 0.24,
            "tiles": moving_tiles,
        }

    def update(self, dt):
        events = {
            "score_delta": 0,
            "move_completed": False,
            "shuffle_happened": False,
        }

        if self.swap_animation is not None:
            self.swap_animation["elapsed"] += dt

            if self.swap_animation["elapsed"] >= self.swap_animation["duration"]:
                finished_return = self.swap_animation["is_return"]
                first = self.swap_animation["first"]
                second = self.swap_animation["second"]
                self.swap_animation = None

                if finished_return:
                    self.completed_player_move = False
                else:
                    matches = self.find_matches()
                    if matches:
                        self.completed_player_move = True
                        self.start_remove_animation(matches, chain_multiplier=1)
                    else:
                        self.start_swap_animation(first, second, is_return=True)

        elif self.remove_animation is not None:
            self.remove_animation["elapsed"] += dt

            if self.remove_animation["elapsed"] >= self.remove_animation["duration"]:
                for row, col in self.current_matches:
                    self.grid[row][col] = None

                events["score_delta"] += self.score_to_add
                self.score_to_add = 0
                self.remove_animation = None
                self.build_fall_animation()

        elif self.fall_animation is not None:
            self.fall_animation["elapsed"] += dt

            if self.fall_animation["elapsed"] >= self.fall_animation["duration"]:
                self.fall_animation = None
                new_matches = self.find_matches()

                if new_matches:
                    self.start_remove_animation(new_matches, chain_multiplier=2)
                else:
                    if self.completed_player_move:
                        events["move_completed"] = True
                        self.completed_player_move = False

                    if not self.has_possible_moves():
                        self.shuffle_board()
                        events["shuffle_happened"] = True

        return events

    def draw_gem(self, screen, value, center_x, center_y, size, alpha=255):
        gem_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        color = self.tile_colors[value]
        gem_rect = pygame.Rect(0, 0, size, size)

        pygame.draw.circle(gem_surface, (*color, alpha), gem_rect.center, size // 2 - 3)
        pygame.draw.circle(gem_surface, (255, 248, 235, alpha), gem_rect.center, size // 2 - 3, width=2)

        highlight_rect = pygame.Rect(size * 0.22, size * 0.15, size * 0.25, size * 0.18)
        pygame.draw.ellipse(gem_surface, (255, 255, 255, min(alpha, 170)), highlight_rect)

        screen.blit(gem_surface, (center_x - size // 2, center_y - size // 2))

    def draw(self, screen):
        board_width = self.cols * self.tile_size
        board_height = self.rows * self.tile_size

        board_rect = pygame.Rect(self.x - 8, self.y - 8, board_width + 16, board_height + 16)
        pygame.draw.rect(screen, self.background_color, board_rect, border_radius=18)
        pygame.draw.rect(screen, self.frame_color, board_rect, width=3, border_radius=18)

        for row in range(self.rows):
            for col in range(self.cols):
                cell_rect = pygame.Rect(
                    self.x + col * self.tile_size,
                    self.y + row * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                pygame.draw.rect(screen, self.cell_color, cell_rect.inflate(-6, -6), border_radius=12)

        animated_positions = set()

        if self.swap_animation is not None:
            animated_positions.add(self.swap_animation["first"])
            animated_positions.add(self.swap_animation["second"])

        if self.remove_animation is not None:
            animated_positions.update(self.current_matches)

        if self.fall_animation is not None:
            for tile in self.fall_animation["tiles"]:
                animated_positions.add((tile["end_row"], tile["col"]))

        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in animated_positions:
                    continue

                value = self.grid[row][col]
                if value is None:
                    continue

                center_x = self.x + col * self.tile_size + self.tile_size // 2
                center_y = self.y + row * self.tile_size + self.tile_size // 2
                self.draw_gem(screen, value, center_x, center_y, self.tile_size - 16)

        if self.selected_cell is not None:
            row, col = self.selected_cell
            selected_rect = pygame.Rect(
                self.x + col * self.tile_size + 4,
                self.y + row * self.tile_size + 4,
                self.tile_size - 8,
                self.tile_size - 8,
            )
            pygame.draw.rect(screen, (255, 245, 190), selected_rect, width=3, border_radius=12)

        if self.swap_animation is not None:
            progress = min(1.0, self.swap_animation["elapsed"] / self.swap_animation["duration"])

            first_row, first_col = self.swap_animation["first"]
            second_row, second_col = self.swap_animation["second"]

            first_start_x = self.x + first_col * self.tile_size + self.tile_size // 2
            first_start_y = self.y + first_row * self.tile_size + self.tile_size // 2
            second_start_x = self.x + second_col * self.tile_size + self.tile_size // 2
            second_start_y = self.y + second_row * self.tile_size + self.tile_size // 2

            first_x = first_start_x + (second_start_x - first_start_x) * progress
            first_y = first_start_y + (second_start_y - first_start_y) * progress
            second_x = second_start_x + (first_start_x - second_start_x) * progress
            second_y = second_start_y + (first_start_y - second_start_y) * progress

            self.draw_gem(
                screen,
                self.swap_animation["second_value"],
                int(first_x),
                int(first_y),
                self.tile_size - 16,
            )
            self.draw_gem(
                screen,
                self.swap_animation["first_value"],
                int(second_x),
                int(second_y),
                self.tile_size - 16,
            )

        if self.remove_animation is not None:
            progress = min(1.0, self.remove_animation["elapsed"] / self.remove_animation["duration"])
            alpha = int(255 * (1.0 - progress))
            size = int((self.tile_size - 16) * (1.0 - progress * 0.25))

            for row, col in self.current_matches:
                value = self.grid[row][col]
                if value is None:
                    continue

                center_x = self.x + col * self.tile_size + self.tile_size // 2
                center_y = self.y + row * self.tile_size + self.tile_size // 2
                self.draw_gem(screen, value, center_x, center_y, size, alpha=alpha)

        if self.fall_animation is not None:
            progress = min(1.0, self.fall_animation["elapsed"] / self.fall_animation["duration"])
            ease = 1.0 - (1.0 - progress) * (1.0 - progress)

            for tile in self.fall_animation["tiles"]:
                start_y = self.y + tile["start_row"] * self.tile_size + self.tile_size // 2
                end_y = self.y + tile["end_row"] * self.tile_size + self.tile_size // 2
                center_y = start_y + (end_y - start_y) * ease
                center_x = self.x + tile["col"] * self.tile_size + self.tile_size // 2

                self.draw_gem(screen, tile["value"], int(center_x), int(center_y), self.tile_size - 16)
