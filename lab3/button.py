import pygame


class Button:
    def __init__(self, rect, text, font, fill_color, hover_color, text_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.fill_color = fill_color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, screen, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.fill_color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (245, 236, 210), self.rect, width=2, border_radius=12)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
