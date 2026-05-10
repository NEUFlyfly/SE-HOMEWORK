from __future__ import annotations

import pygame

from core.models import Furniture, Interaction, SceneData


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
        initial_dialogue="场景二占位：靠近书桌后按 Space 互动。",
    )
