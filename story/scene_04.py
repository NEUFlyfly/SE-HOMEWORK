from __future__ import annotations

from collections.abc import Sequence

import pygame

from core.constants import COLORS, ROOM_RECT
from core.models import Furniture, Interaction, SceneData, SceneFontBook


def draw_scene_04_background(
    surface: pygame.Surface,
    furniture: Sequence[Furniture],
    fonts: SceneFontBook,
) -> None:
    _ = furniture, fonts
    surface.fill((37, 30, 43))
    pygame.draw.rect(surface, (78, 51, 72), ROOM_RECT.inflate(32, 32), border_radius=6)
    pygame.draw.rect(surface, (132, 83, 94), ROOM_RECT, border_radius=4)

    pygame.draw.rect(surface, (87, 51, 70), (ROOM_RECT.x, ROOM_RECT.y, ROOM_RECT.width, 126))
    for x in range(ROOM_RECT.x + 28, ROOM_RECT.right, 62):
        pygame.draw.circle(surface, (171, 111, 104), (x, ROOM_RECT.y + 54), 18)
        pygame.draw.circle(surface, (99, 61, 76), (x + 20, ROOM_RECT.y + 84), 14)

    floor = pygame.Rect(ROOM_RECT.x + 20, ROOM_RECT.y + 126, ROOM_RECT.width - 40, ROOM_RECT.height - 146)
    pygame.draw.rect(surface, (104, 70, 67), floor)
    for x in range(floor.x, floor.right, 40):
        pygame.draw.line(surface, (138, 91, 80), (x, floor.y), (x + 74, floor.bottom), 2)

    stage = pygame.Rect(312, 406, 420, 78)
    pygame.draw.rect(surface, (71, 45, 58), stage, border_radius=8)
    pygame.draw.rect(surface, COLORS["gold"], stage.inflate(-18, -18), 3, border_radius=6)
    pygame.draw.rect(surface, (218, 163, 103), (132, 116, 110, 92), border_radius=6)
    pygame.draw.rect(surface, COLORS["ink"], (132, 116, 110, 92), 3, border_radius=6)
    pygame.draw.line(surface, (107, 73, 70), (154, 158), (218, 158), 4)


def scene_04() -> SceneData:
    sofa_rect = pygame.Rect(582, 394, 148, 92)

    return SceneData(
        scene_id="scene_04",
        title="人生记忆回廊 · 场景四占位",
        spawn=(488, 420),
        furniture=(
            Furniture(
                "待叙述的沙发",
                sofa_rect,
                "sofa",
                Interaction(
                    "待叙述的沙发",
                    sofa_rect.inflate(36, 32),
                    "按 Space 靠近沙发",
                    ("这里会承接第四段记忆的故事。",),
                    "待叙述的故事",
                ),
            ),
        ),
        draw_background=draw_scene_04_background,
        initial_dialogue="场景四占位：靠近沙发后按 Space 互动。",
    )
