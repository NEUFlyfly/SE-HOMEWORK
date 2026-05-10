from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

import pygame

from core.constants import COLORS, GROWTH_PANEL_RECT, HEIGHT, ROOM_RECT, WIDTH
from core.dialogue import DialogueState
from core.models import Furniture, Interaction, SceneData
from core.player import Player
from rendering.prop_drawers import draw_furniture
from rendering.ui import FontBook, draw_panel, draw_text


class DrawableClueSpark(Protocol):
    @property
    def progress(self) -> float: ...

    @property
    def position(self) -> pygame.Vector2: ...


class RoomRenderer:
    def __init__(self, fonts: FontBook) -> None:
        self.fonts = fonts

    def draw(
        self,
        screen: pygame.Surface,
        scene_data: SceneData,
        furniture: list[Furniture],
        player: Player,
        active: Interaction | None,
        dialogue: DialogueState,
        clue_order: list[str],
        collected_clues: list[str],
        clue_sparks: Sequence[DrawableClueSpark],
    ) -> None:
        world = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self._draw_world(world, scene_data, furniture, player, active, dialogue, clue_order, collected_clues, clue_sparks)
        pygame.transform.smoothscale(world, screen.get_size(), screen)

    def _draw_world(
        self,
        surface: pygame.Surface,
        scene_data: SceneData,
        furniture: list[Furniture],
        player: Player,
        active: Interaction | None,
        dialogue: DialogueState,
        clue_order: list[str],
        collected_clues: list[str],
        clue_sparks: Sequence[DrawableClueSpark],
    ) -> None:
        surface.fill((34, 30, 33))
        self._draw_room_shell(surface)
        self._draw_floor(surface)
        self._draw_wall_details(surface, furniture)

        drawables: list[tuple[int, str, Furniture | None]] = [
            (item.rect.bottom, "furniture", item) for item in furniture
        ]
        drawables.append((player.feet_rect.bottom, "player", None))
        for _, kind, item in sorted(drawables, key=lambda drawable: drawable[0]):
            if kind == "player":
                player.draw(surface)
            elif item:
                draw_furniture(surface, item)

        self._draw_foreground_details(surface)
        self._draw_growth_track(surface, clue_order, collected_clues)
        self._draw_clue_sparks(surface, clue_sparks)
        self._draw_ui(surface, scene_data, active, dialogue)

    def _draw_room_shell(self, surface: pygame.Surface) -> None:
        outer = ROOM_RECT.inflate(28, 28)
        pygame.draw.rect(surface, COLORS["wood_dark"], outer, border_radius=4)
        pygame.draw.rect(surface, COLORS["wall"], ROOM_RECT, border_radius=2)
        pygame.draw.rect(surface, COLORS["ink"], outer, 4, border_radius=4)
        pygame.draw.rect(surface, COLORS["wall_dark"], (ROOM_RECT.x, ROOM_RECT.y, ROOM_RECT.width, 96))
        pygame.draw.rect(surface, COLORS["wood_dark"], (ROOM_RECT.x, ROOM_RECT.y + 94, ROOM_RECT.width, 8))

    def _draw_floor(self, surface: pygame.Surface) -> None:
        floor = pygame.Rect(ROOM_RECT.x + 20, ROOM_RECT.y + 102, ROOM_RECT.width - 40, ROOM_RECT.height - 122)
        pygame.draw.rect(surface, COLORS["floor_a"], floor)
        tile = 32
        for y in range(floor.y, floor.bottom, tile):
            for x in range(floor.x, floor.right, tile):
                color = COLORS["floor_b"] if (x // tile + y // tile) % 2 else COLORS["floor_a"]
                pygame.draw.rect(surface, color, (x, y, tile, tile))
                pygame.draw.rect(surface, (178, 127, 78), (x, y, tile, tile), 1)

        rug = pygame.Rect(366, 326, 218, 118)
        pygame.draw.rect(surface, COLORS["red_dark"], rug, border_radius=4)
        pygame.draw.rect(surface, COLORS["red"], rug.inflate(-12, -12), border_radius=4)
        pygame.draw.rect(surface, COLORS["gold"], rug.inflate(-30, -30), 4, border_radius=4)
        for x in range(rug.x + 26, rug.right - 20, 22):
            pygame.draw.circle(surface, COLORS["cream"], (x, rug.centery), 3)

    def _draw_wall_details(self, surface: pygame.Surface, furniture: list[Furniture]) -> None:
        pygame.draw.rect(surface, COLORS["wood_light"], (122, 94, 78, 42), border_radius=2)
        pygame.draw.rect(surface, COLORS["ink"], (122, 94, 78, 42), 3, border_radius=2)
        draw_text(surface, "练琴日程", (126, 95), self.fonts.small, COLORS["paper"])
        draw_text(surface, "1  2  3  4", (126, 110), self.fonts.small, (231, 205, 162))

        window = next((item for item in furniture if item.kind == "window"), None)
        if window is None:
            return

        frame = window.rect
        pygame.draw.rect(surface, COLORS["wood_dark"], frame.inflate(10, 10), border_radius=3)
        pygame.draw.rect(surface, COLORS["glass"], frame, border_radius=2)
        pygame.draw.circle(surface, (249, 199, 112), (frame.x + 26, frame.y + 20), 12)
        pygame.draw.line(surface, COLORS["glass_light"], (frame.x + 10, frame.y + 12), (frame.x + 76, frame.y + 12), 4)
        pygame.draw.line(surface, COLORS["glass_light"], (frame.x + 94, frame.y + 12), (frame.x + 164, frame.y + 12), 4)
        pygame.draw.line(surface, COLORS["wood_dark"], frame.midtop, frame.midbottom, 5)
        pygame.draw.line(surface, COLORS["wood_dark"], frame.midleft, frame.midright, 5)
        pygame.draw.rect(surface, COLORS["ink"], frame.inflate(10, 10), 3, border_radius=3)

    def _draw_foreground_details(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, COLORS["wood_dark"], (ROOM_RECT.centerx - 44, ROOM_RECT.bottom - 28, 88, 24))
        pygame.draw.rect(surface, COLORS["gold"], (ROOM_RECT.centerx - 10, ROOM_RECT.bottom - 22, 20, 8), border_radius=2)

    def _draw_growth_track(self, surface: pygame.Surface, clue_order: list[str], collected_clues: list[str]) -> None:
        panel = GROWTH_PANEL_RECT
        pygame.draw.line(surface, (*COLORS["gold"],), (panel.x + 2, panel.y + 18), (panel.x + 2, panel.bottom - 18), 2)
        pygame.draw.line(surface, COLORS["wood_dark"], (panel.x + 10, panel.y + 52), (panel.x + 10, panel.bottom - 34), 3)
        draw_text(surface, "成长轨迹", (panel.x + 34, panel.y + 24), self.fonts.body, COLORS["paper"])
        draw_text(surface, "收集童年的声音", (panel.x + 36, panel.y + 52), self.fonts.small, (231, 205, 162))

        top = panel.y + 78
        bottom = panel.bottom - 34
        total = len(clue_order)
        for index, label in enumerate(clue_order):
            if total <= 1:
                y = top
            else:
                y = top + round(index * ((bottom - top) / (total - 1)))
            collected = label in collected_clues
            color = COLORS["amber"] if collected else (118, 91, 71)
            pygame.draw.circle(surface, color, (panel.x + 34, y), 8 if collected else 5)
            if collected:
                pygame.draw.circle(surface, COLORS["paper"], (panel.x + 34, y), 3)
                draw_text(surface, label, (panel.x + 52, y - 11), self.fonts.small, COLORS["paper"])
            else:
                pygame.draw.circle(surface, COLORS["wood_dark"], (panel.x + 34, y), 5, 1)
                draw_text(surface, "待发现", (panel.x + 52, y - 11), self.fonts.small, (137, 104, 82))

    def _draw_clue_sparks(self, surface: pygame.Surface, clue_sparks: Sequence[DrawableClueSpark]) -> None:
        for spark in clue_sparks:
            position = spark.position
            progress = spark.progress
            radius = max(4, round(12 * (1 - progress) + 4))
            alpha = max(40, round(230 * (1 - progress) + 25))
            glow = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
            center = (radius * 2, radius * 2)
            pygame.draw.circle(glow, (*COLORS["amber"], alpha // 3), center, radius * 2)
            pygame.draw.circle(glow, (*COLORS["paper"], alpha), center, radius)
            surface.blit(glow, (round(position.x) - radius * 2, round(position.y) - radius * 2))

    def _draw_ui(
        self,
        surface: pygame.Surface,
        scene_data: SceneData,
        active: Interaction | None,
        dialogue: DialogueState,
    ) -> None:
        draw_panel(surface, pygame.Rect(58, 18, 470, 48), alpha=220)
        draw_text(surface, scene_data.title, (78, 28), self.fonts.body, COLORS["paper"])

        hint = "方向键/WASD 移动   Space 收集线索   Esc 退出"
        draw_panel(surface, pygame.Rect(574, 18, 360, 48), alpha=210)
        draw_text(surface, hint, (592, 31), self.fonts.small, COLORS["paper"])

        panel = pygame.Rect(82, 566, 796, 68)
        draw_panel(surface, panel, alpha=232)
        text = active.prompt if active else dialogue.text
        text_pos = (130, 558) if active else (110, 558)
        if active:
            pygame.draw.circle(surface, (42, 30, 27), (117, 572), 6)
            pygame.draw.circle(surface, COLORS["paper"], (115, 570), 5)
        draw_text(surface, text, text_pos, self.fonts.body, COLORS["paper"])
        if active and dialogue.owner == active.name:
            draw_text(surface, dialogue.text, (110, 586), self.fonts.small, (231, 205, 162))
