from __future__ import annotations

import pygame

from core.constants import COLORS


class FontBook:
    def __init__(self) -> None:
        names = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Arial Unicode MS"]
        self.title = self._font(names, 32, bold=True)
        self.body = self._font(names, 21)
        self.small = self._font(names, 17)

    @staticmethod
    def _font(names: list[str], size: int, bold: bool = False) -> pygame.font.Font:
        for name in names:
            match = pygame.font.match_font(name, bold=bold)
            if match:
                return pygame.font.Font(match, size)
        return pygame.font.Font(None, size)


def draw_panel(surface: pygame.Surface, rect: pygame.Rect, alpha: int) -> None:
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(panel, (*COLORS["wood_dark"], alpha), panel.get_rect(), border_radius=8)
    pygame.draw.rect(panel, (*COLORS["gold"], alpha), panel.get_rect().inflate(-8, -8), 2, border_radius=6)
    pygame.draw.rect(panel, (*COLORS["ink"], alpha), panel.get_rect(), 3, border_radius=8)
    surface.blit(panel, rect)


def draw_text(
    surface: pygame.Surface,
    text: str,
    pos: tuple[int, int],
    font: pygame.font.Font,
    color: tuple[int, int, int],
) -> None:
    shadow = font.render(text, True, (42, 30, 27))
    surface.blit(shadow, (pos[0] + 2, pos[1] + 2))
    rendered = font.render(text, True, color)
    surface.blit(rendered, pos)
