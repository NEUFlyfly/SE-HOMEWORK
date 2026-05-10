from __future__ import annotations

import pygame

from core.models import Furniture, Interaction, SceneData


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
        initial_dialogue="场景三占位：靠近木柜后按 Space 互动。",
    )
