from __future__ import annotations

import pygame

from minigames.adapter import MiniGameResult, run_minigame


class StoryFlow:
    def __init__(self) -> None:
        self.backtrack_results: dict[int, MiniGameResult] = {}

    def run_backtrack_node(self, node_id: int, screen: pygame.Surface, clock: pygame.time.Clock) -> MiniGameResult:
        result = run_minigame(node_id, screen, clock)
        self.backtrack_results[node_id] = result
        return result
