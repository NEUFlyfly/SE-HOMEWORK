from __future__ import annotations

from collections.abc import Sequence

import pygame

from core.constants import COLORS, ROOM_RECT
from core.models import Furniture, Interaction, SceneData, SceneFontBook


def draw_scene_03_background(
    surface: pygame.Surface,
    furniture: Sequence[Furniture],
    fonts: SceneFontBook,
) -> None:
    _ = furniture, fonts
    surface.fill((30, 28, 36))
    pygame.draw.rect(surface, (41, 58, 50), ROOM_RECT.inflate(28, 28), border_radius=8)
    pygame.draw.rect(surface, (76, 111, 83), ROOM_RECT, border_radius=4)

    ceiling = pygame.Rect(ROOM_RECT.x, ROOM_RECT.y, ROOM_RECT.width, 116)
    pygame.draw.rect(surface, (40, 77, 72), ceiling)
    for x in range(ROOM_RECT.x + 38, ROOM_RECT.right, 92):
        pygame.draw.line(surface, (116, 155, 123), (x, ROOM_RECT.y + 16), (x - 36, ROOM_RECT.y + 104), 3)

    floor = pygame.Rect(ROOM_RECT.x + 18, ROOM_RECT.y + 118, ROOM_RECT.width - 36, ROOM_RECT.height - 138)
    pygame.draw.rect(surface, (89, 68, 57), floor)
    for y in range(floor.y + 18, floor.bottom, 36):
        pygame.draw.line(surface, (122, 92, 69), (floor.x, y), (floor.right, y + 18), 2)

    carpet = pygame.Rect(394, 352, 260, 116)
    pygame.draw.rect(surface, (48, 88, 85), carpet, border_radius=50)
    pygame.draw.rect(surface, (166, 137, 81), carpet.inflate(-18, -18), 3, border_radius=42)
    for x in range(carpet.x + 44, carpet.right - 36, 36):
        pygame.draw.circle(surface, (209, 187, 132), (x, carpet.centery), 4)

    pygame.draw.rect(surface, (182, 159, 104), (590, 102, 134, 66), border_radius=5)
    pygame.draw.rect(surface, COLORS["ink"], (590, 102, 134, 66), 3, border_radius=5)
    pygame.draw.circle(surface, (255, 218, 126), (626, 132), 16)


def scene_03() -> SceneData:
    cabinet_rect = pygame.Rect(176, 186, 128, 96)

    return SceneData(
        scene_id="scene_03",
        title="人生记忆回廊 · 场景三占位",
        spawn=(520, 420),
        furniture=(
            Furniture(
                "待整理的木柜",
                cabinet_rect,
                "cabinet",
                Interaction(
                    "待整理的木柜",
                    cabinet_rect.inflate(32, 30),
                    "按 Space 查看木柜",
                    ("木柜里还留着未来场景要展开的线索。",),
                    "未整理的线索",
                ),
            ),
        ),
        draw_background=draw_scene_03_background,
        initial_dialogue="场景三占位：靠近木柜后按 Space 互动。",
    )
