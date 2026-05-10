from __future__ import annotations

import pygame

from core.constants import COLORS
from core.models import Furniture


def draw_furniture(surface: pygame.Surface, item: Furniture) -> None:
    rect = item.rect
    if item.kind == "piano":
        pygame.draw.rect(surface, COLORS["wood_dark"], rect.inflate(12, 16), border_radius=6)
        pygame.draw.rect(surface, COLORS["wood"], rect, border_radius=4)
        pygame.draw.rect(surface, COLORS["wood_light"], (rect.x + 14, rect.y + 12, rect.width - 28, 24), border_radius=3)
        pygame.draw.rect(surface, COLORS["paper"], (rect.x + 74, rect.y - 18, 58, 32), border_radius=2)
        pygame.draw.line(surface, COLORS["ink"], (rect.x + 84, rect.y - 8), (rect.x + 120, rect.y - 8), 2)
        pygame.draw.line(surface, COLORS["ink"], (rect.x + 84, rect.y + 2), (rect.x + 126, rect.y + 2), 2)
        pygame.draw.circle(surface, COLORS["amber"], (rect.x + 30, rect.y + 24), 5)
        keys = pygame.Rect(rect.x + 18, rect.y + 48, rect.width - 36, 22)
        pygame.draw.rect(surface, COLORS["cream"], keys)
        for x in range(keys.x + 8, keys.right, 13):
            pygame.draw.rect(surface, COLORS["ink"], (x, keys.y, 6, 14))
        pygame.draw.rect(surface, COLORS["ink"], rect.inflate(12, 16), 3, border_radius=6)
    elif item.kind == "chair":
        pygame.draw.rect(surface, COLORS["wood_dark"], (rect.x + 6, rect.y + 2, 7, 50), border_radius=2)
        pygame.draw.rect(surface, COLORS["wood_dark"], (rect.right - 13, rect.y + 2, 7, 50), border_radius=2)
        pygame.draw.rect(surface, COLORS["wood"], (rect.x + 6, rect.y, rect.width - 12, 22), border_radius=4)
        pygame.draw.rect(surface, COLORS["wood_light"], (rect.x + 10, rect.y + 4, rect.width - 20, 12), border_radius=3)
        pygame.draw.rect(surface, COLORS["wood_dark"], (rect.x + 5, rect.y + 42, rect.width - 10, 8), border_radius=3)
        pygame.draw.rect(surface, COLORS["red_dark"], (rect.x + 9, rect.y + 25, rect.width - 18, 20), border_radius=5)
        pygame.draw.rect(surface, COLORS["red"], (rect.x + 11, rect.y + 27, rect.width - 22, 15), border_radius=4)
        pygame.draw.rect(surface, COLORS["wood"], (rect.x + 9, rect.y + 48, 8, 14), border_radius=2)
        pygame.draw.rect(surface, COLORS["wood"], (rect.right - 17, rect.y + 48, 8, 14), border_radius=2)
    elif item.kind == "shelf":
        pygame.draw.rect(surface, COLORS["wood_dark"], rect, border_radius=3)
        pygame.draw.rect(surface, COLORS["wood"], rect.inflate(-10, -10), border_radius=2)
        for y in (rect.y + 46, rect.y + 88, rect.y + 130):
            pygame.draw.line(surface, COLORS["wood_light"], (rect.x + 8, y), (rect.right - 8, y), 5)
        for i, color in enumerate((COLORS["blue"], COLORS["red"], COLORS["green"], COLORS["cream"])):
            pygame.draw.rect(surface, color, (rect.x + 18 + i * 18, rect.y + 20, 12, 25))
        pygame.draw.circle(surface, COLORS["gold"], (rect.right - 28, rect.y + 70), 10)
        pygame.draw.line(surface, COLORS["ink"], (rect.right - 28, rect.y + 58), (rect.right - 28, rect.y + 82), 2)
        pygame.draw.line(surface, COLORS["ink"], (rect.right - 40, rect.y + 70), (rect.right - 16, rect.y + 70), 2)
        pygame.draw.rect(surface, COLORS["ink"], rect, 3, border_radius=3)
    elif item.kind == "table":
        pygame.draw.rect(surface, COLORS["wood_dark"], rect.inflate(8, 8), border_radius=12)
        pygame.draw.rect(surface, COLORS["wood_light"], rect, border_radius=10)
        pygame.draw.rect(surface, COLORS["paper"], (rect.x + 26, rect.y + 18, 46, 32), border_radius=2)
        pygame.draw.line(surface, COLORS["ink"], (rect.x + 34, rect.y + 28), (rect.x + 62, rect.y + 28), 2)
        pygame.draw.line(surface, COLORS["ink"], (rect.x + 36, rect.y + 38), (rect.x + 58, rect.y + 38), 2)
        pygame.draw.line(surface, COLORS["red_dark"], (rect.x + 78, rect.y + 48), (rect.x + 104, rect.y + 30), 4)
        pygame.draw.circle(surface, COLORS["cream"], (rect.right - 28, rect.y + 28), 13)
        pygame.draw.circle(surface, COLORS["paper"], (rect.right - 28, rect.y + 28), 5)
        pygame.draw.rect(surface, COLORS["ink"], rect.inflate(8, 8), 3, border_radius=12)
    elif item.kind == "plant":
        pygame.draw.rect(surface, COLORS["wood_light"], (rect.x + 12, rect.y + 42, 30, 30), border_radius=4)
        pygame.draw.circle(surface, COLORS["green"], (rect.centerx, rect.y + 20), 22)
        pygame.draw.circle(surface, (68, 112, 68), (rect.x + 18, rect.y + 28), 16)
        pygame.draw.circle(surface, (114, 155, 93), (rect.right - 16, rect.y + 28), 14)
        pygame.draw.line(surface, COLORS["glass_light"], (rect.centerx, rect.y + 12), (rect.centerx - 10, rect.y + 30), 2)
        pygame.draw.line(surface, COLORS["glass_light"], (rect.centerx, rect.y + 12), (rect.centerx + 13, rect.y + 28), 2)
        pygame.draw.rect(surface, COLORS["ink"], (rect.x + 12, rect.y + 42, 30, 30), 3, border_radius=4)
    elif item.kind == "bed":
        pygame.draw.rect(surface, COLORS["wood_dark"], rect.inflate(8, 8), border_radius=7)
        pygame.draw.rect(surface, COLORS["wood"], (rect.x - 2, rect.y - 2, rect.width + 4, 18), border_radius=5)
        pygame.draw.rect(surface, COLORS["wood"], (rect.x - 2, rect.y + 52, rect.width + 4, 20), border_radius=5)
        pygame.draw.rect(surface, COLORS["cream"], (rect.x + 6, rect.y + 8, rect.width - 12, 54), border_radius=5)
        pygame.draw.rect(surface, COLORS["paper"], (rect.x + 14, rect.y + 14, 40, 24), border_radius=5)
        pygame.draw.rect(surface, COLORS["paper"], (rect.x + 58, rect.y + 14, 34, 22), border_radius=5)
        pygame.draw.rect(surface, COLORS["red_dark"], (rect.x + 10, rect.y + 34, rect.width - 20, 30), border_radius=4)
        pygame.draw.rect(surface, COLORS["red"], (rect.x + 14, rect.y + 32, rect.width - 28, 24), border_radius=4)
        pygame.draw.line(surface, COLORS["cream"], (rect.x + 24, rect.y + 38), (rect.right - 24, rect.y + 38), 2)
        for x in range(rect.x + 30, rect.right - 24, 28):
            pygame.draw.circle(surface, COLORS["gold"], (x, rect.y + 48), 3)
        pygame.draw.rect(surface, COLORS["wood_light"], (rect.x + 8, rect.y + 2, rect.width - 16, 6), border_radius=3)
