from __future__ import annotations

import pygame

from core.character_animation import CharacterAnimationConfig, CharacterAnimator
from core.constants import PLAYER_SIZE, ROOM_RECT


class Player:
    def __init__(self, spawn: tuple[int, int]) -> None:
        self.pos = pygame.Vector2(spawn)
        self.speed = 210.0
        self.facing = pygame.Vector2(0, 1)
        self.step_timer = 0.0
        self.animator = CharacterAnimator(CharacterAnimationConfig("Julia"))

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.pos.x), round(self.pos.y), *PLAYER_SIZE)

    @property
    def feet_rect(self) -> pygame.Rect:
        rect = self.rect
        return pygame.Rect(rect.x + 12, rect.bottom - 18, rect.width - 24, 14)

    def move(self, direction: pygame.Vector2, dt: float, blockers: list[pygame.Rect]) -> None:
        if direction.length_squared() == 0:
            self.step_timer = 0.0
            self.animator.update(direction, dt)
            return

        direction = direction.normalize()
        self.facing = direction
        self.step_timer += dt
        self.animator.update(direction, dt)

        old_x = self.pos.x
        self.pos.x += direction.x * self.speed * dt
        if self._blocked(blockers):
            self.pos.x = old_x

        old_y = self.pos.y
        self.pos.y += direction.y * self.speed * dt
        if self._blocked(blockers):
            self.pos.y = old_y

    def _blocked(self, blockers: list[pygame.Rect]) -> bool:
        feet = self.feet_rect
        if not ROOM_RECT.contains(feet):
            return True
        return any(feet.colliderect(blocker) for blocker in blockers)

    def draw(self, surface: pygame.Surface) -> None:
        rect = self.rect
        bob = 0
        if self.step_timer:
            bob = -2 if int(self.step_timer * 12) % 2 == 0 else 0
        shadow = pygame.Rect(rect.x + 8, rect.bottom - 14, rect.width - 16, 12)
        pygame.draw.ellipse(surface, (0, 0, 0, 55), shadow)
        surface.blit(self.animator.image, (rect.x, rect.y + bob))
