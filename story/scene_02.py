from __future__ import annotations

from collections.abc import Sequence

import pygame

from core.constants import COLORS, HEIGHT, ROOM_RECT, WIDTH
from core.models import Furniture, Interaction, SceneData, SceneFontBook


def draw_scene_02_background(
    surface: pygame.Surface,
    furniture: Sequence[Furniture],
    fonts: SceneFontBook,
) -> None:
    _ = furniture, fonts
    surface.fill((28, 34, 44))
    pygame.draw.rect(surface, (48, 63, 84), ROOM_RECT.inflate(30, 30), border_radius=6)
    pygame.draw.rect(surface, (112, 142, 160), ROOM_RECT, border_radius=4)
    pygame.draw.rect(surface, (72, 92, 112), (ROOM_RECT.x, ROOM_RECT.y, ROOM_RECT.width, 118))
    pygame.draw.rect(surface, (38, 46, 58), (ROOM_RECT.x, ROOM_RECT.y + 116, ROOM_RECT.width, 8))

    floor = pygame.Rect(ROOM_RECT.x + 24, ROOM_RECT.y + 124, ROOM_RECT.width - 48, ROOM_RECT.height - 144)
    pygame.draw.rect(surface, (170, 148, 112), floor)
    for y in range(floor.y, floor.bottom, 34):
        pygame.draw.line(surface, (137, 116, 88), (floor.x, y), (floor.right, y), 1)
    for x in range(floor.x, floor.right, 68):
        pygame.draw.line(surface, (184, 162, 124), (x, floor.y), (x - 42, floor.bottom), 1)

    board = pygame.Rect(120, 110, 184, 80)
    pygame.draw.rect(surface, (246, 225, 174), board, border_radius=4)
    pygame.draw.rect(surface, COLORS["ink"], board, 3, border_radius=4)
    pygame.draw.line(surface, (91, 108, 130), (board.x + 20, board.y + 28), (board.right - 18, board.y + 28), 3)
    pygame.draw.line(surface, (91, 108, 130), (board.x + 20, board.y + 50), (board.right - 42, board.y + 50), 3)

    lamp = pygame.Rect(WIDTH - 500, 116, 78, 54)
    pygame.draw.ellipse(surface, (255, 224, 128), lamp)
    pygame.draw.line(surface, (74, 59, 48), lamp.midtop, (lamp.centerx, ROOM_RECT.y), 4)
    pygame.draw.rect(surface, (75, 55, 47), (ROOM_RECT.centerx - 48, HEIGHT - 96, 96, 18), border_radius=4)


def scene_02() -> SceneData:
    desk_rect = pygame.Rect(334, 246, 132, 104)

    return SceneData(
        scene_id="scene_02",
        title="人生记忆回廊 · 场景二占位",
        spawn=(520, 420),
        furniture=(
            Furniture(
                "待写的书桌",
                desk_rect,
                "desk",
                Interaction(
                    "待写的书桌",
                    desk_rect.inflate(36, 34),
                    "按 Space 查看书桌",
                    ("这张书桌等待新的记忆被写下。",),
                    "待写的记忆",
                ),
            ),
        ),
        draw_background=draw_scene_02_background,
        initial_dialogue="场景二占位：靠近书桌后按 Space 互动。",
    )
