from __future__ import annotations

import pygame

from minigames.adapter import MiniGameResult


def run_placeholder_minigame(node_id: int, screen: pygame.Surface, clock: pygame.time.Clock) -> MiniGameResult:
    return MiniGameResult(success=True, info={"node_id": node_id, "mode": "placeholder"})
