from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class MiniGameResult:
    success: bool
    info: dict[str, object] | None = None


def run_minigame(node_id: int, screen: pygame.Surface, clock: pygame.time.Clock) -> MiniGameResult:
    from minigames.placeholder import run_placeholder_minigame

    return run_placeholder_minigame(node_id, screen, clock)
