from __future__ import annotations

import pygame

from core.models import Furniture, Interaction, SceneData


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
        initial_dialogue="场景四占位：靠近沙发后按 Space 互动。",
    )
