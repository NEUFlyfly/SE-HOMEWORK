from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class Interaction:
    name: str
    rect: pygame.Rect
    prompt: str
    lines: tuple[str, ...]
    clue_label: str


@dataclass(frozen=True)
class Furniture:
    name: str
    rect: pygame.Rect
    kind: str
    interaction: Interaction | None = None


@dataclass(frozen=True)
class SceneData:
    scene_id: str
    title: str
    spawn: tuple[int, int]
    furniture: tuple[Furniture, ...]
    initial_dialogue: str
