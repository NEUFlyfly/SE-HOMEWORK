from __future__ import annotations

from dataclasses import dataclass

import pygame

from core.constants import CLUE_SPARK_DURATION, GROWTH_PANEL_RECT, ROOM_RECT
from core.dialogue import DialogueState
from core.models import Interaction, SceneData
from core.player import Player
from rendering.renderer import RoomRenderer
from rendering.ui import FontBook


@dataclass
class ClueSpark:
    label: str
    start: pygame.Vector2
    end: pygame.Vector2
    elapsed: float = 0.0

    @property
    def progress(self) -> float:
        return min(1.0, self.elapsed / CLUE_SPARK_DURATION)

    @property
    def position(self) -> pygame.Vector2:
        t = self.progress
        eased = 1 - (1 - t) * (1 - t)
        lift = pygame.Vector2(0, -54 * (1 - abs(0.5 - t) * 2))
        return self.start.lerp(self.end, eased) + lift


class StoryRoomScene:
    def __init__(self, scene_data: SceneData) -> None:
        self.data = scene_data
        self.player = Player(scene_data.spawn)
        self.fonts = FontBook()
        self.renderer = RoomRenderer(self.fonts)
        self.dialogue = DialogueState(scene_data.initial_dialogue)
        self.furniture = list(scene_data.furniture)
        self.clue_order = [item.interaction.clue_label for item in self.furniture if item.interaction]
        self.collected_clues: list[str] = []
        self.clue_sparks: list[ClueSpark] = []
        self.blockers = [item.rect for item in self.furniture]
        self.wall_blockers = [
            pygame.Rect(ROOM_RECT.x, ROOM_RECT.y, ROOM_RECT.width, 20),
            pygame.Rect(ROOM_RECT.x, ROOM_RECT.bottom - 20, ROOM_RECT.width, 20),
            pygame.Rect(ROOM_RECT.x, ROOM_RECT.y, 20, ROOM_RECT.height),
            pygame.Rect(ROOM_RECT.right - 20, ROOM_RECT.y, 20, ROOM_RECT.height),
        ]

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_SPACE:
                target = self.nearby_interaction()
                if target:
                    self.dialogue.advance(target)
                    self._collect_clue(target)
                else:
                    self.dialogue.set_ambient("这里很安静，只听得到木地板轻轻作响。")
        return True

    def update(self, dt: float) -> None:
        self._update_clue_sparks(dt)
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1
        self.player.move(direction, dt, self.blockers + self.wall_blockers)

    def _collect_clue(self, interaction: Interaction) -> None:
        if interaction.clue_label in self.collected_clues:
            return
        self.collected_clues.append(interaction.clue_label)
        slot_index = self.clue_order.index(interaction.clue_label)
        self.clue_sparks.append(
            ClueSpark(
                interaction.clue_label,
                pygame.Vector2(interaction.rect.center),
                pygame.Vector2(self._growth_slot_center(slot_index)),
            )
        )

    def _growth_slot_center(self, slot_index: int) -> tuple[int, int]:
        top = GROWTH_PANEL_RECT.y + 78
        bottom = GROWTH_PANEL_RECT.bottom - 34
        total = len(self.clue_order)
        if total <= 1:
            return (GROWTH_PANEL_RECT.x + 34, top)
        y = top + round(slot_index * ((bottom - top) / (total - 1)))
        return (GROWTH_PANEL_RECT.x + 34, y)

    def _update_clue_sparks(self, dt: float) -> None:
        for spark in self.clue_sparks:
            spark.elapsed += dt
        self.clue_sparks = [spark for spark in self.clue_sparks if spark.progress < 1.0]

    def nearby_interaction(self) -> Interaction | None:
        probe = self.player.feet_rect.inflate(34, 28)
        for item in self.furniture:
            if item.interaction and probe.colliderect(item.interaction.rect):
                return item.interaction
        return None

    def draw(self, screen: pygame.Surface) -> None:
        self.renderer.draw(
            screen,
            self.data,
            self.furniture,
            self.player,
            self.nearby_interaction(),
            self.dialogue,
            self.clue_order,
            self.collected_clues,
            self.clue_sparks,
        )
