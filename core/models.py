from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Protocol

import pygame


class SceneFontBook(Protocol):
    @property
    def title(self) -> pygame.font.Font: ...

    @property
    def body(self) -> pygame.font.Font: ...

    @property
    def small(self) -> pygame.font.Font: ...


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


SceneBackgroundDrawer = Callable[[pygame.Surface, Sequence[Furniture], SceneFontBook], None]


@dataclass(frozen=True)
class SceneData:
    scene_id: str
    title: str
    spawn: tuple[int, int]
    furniture: tuple[Furniture, ...]
    draw_background: SceneBackgroundDrawer
    initial_dialogue: str
