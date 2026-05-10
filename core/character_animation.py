from __future__ import annotations

from dataclasses import dataclass

import pygame

from core.constants import BASE_DIR, COLORS, PLAYER_SIZE


DirectionName = str


@dataclass(frozen=True)
class CharacterAnimationConfig:
    name: str
    frame_size: tuple[int, int] = PLAYER_SIZE
    frame_duration: float = 0.14


class CharacterAnimator:
    directions: tuple[DirectionName, ...] = ("down", "left", "right", "up")
    walk_cycle: tuple[int, ...] = (0, 1, 0, 2)

    def __init__(self, config: CharacterAnimationConfig) -> None:
        self.config = config
        self.frames = self._load_frames(config)
        self.direction: DirectionName = "down"
        self.frame_index = 0
        self.elapsed = 0.0
        self.moving = False

    def update(self, direction: pygame.Vector2, dt: float) -> None:
        self.moving = direction.length_squared() > 0
        if self.moving:
            self.direction = self._direction_name(direction)
            self.elapsed += dt
            if self.elapsed >= self.config.frame_duration:
                self.elapsed %= self.config.frame_duration
                self.frame_index = (self.frame_index + 1) % len(self.walk_cycle)
        else:
            self.elapsed = 0.0
            self.frame_index = 0

    @property
    def image(self) -> pygame.Surface:
        return self.frames[self.direction][self.walk_cycle[self.frame_index]]

    @classmethod
    def _load_frames(cls, config: CharacterAnimationConfig) -> dict[DirectionName, tuple[pygame.Surface, ...]]:
        character_dir = BASE_DIR / "assets" / "images" / config.name
        loaded: dict[DirectionName, tuple[pygame.Surface, ...]] = {}
        for direction in cls.directions:
            frames: list[pygame.Surface] = []
            for index in range(3):
                image_path = character_dir / f"{config.name}-{direction}-{index}.png"
                try:
                    raw = pygame.image.load(str(image_path)).convert_alpha()
                    frames.append(cls._fit_to_frame(raw, config.frame_size))
                except (pygame.error, FileNotFoundError):
                    frames.append(cls._fallback_frame(config.frame_size, direction, index))
            loaded[direction] = tuple(frames)
        return loaded

    @staticmethod
    def _fit_to_frame(raw: pygame.Surface, frame_size: tuple[int, int]) -> pygame.Surface:
        frame = pygame.Surface(frame_size, pygame.SRCALPHA)
        source_width, source_height = raw.get_size()
        scale = min(frame_size[0] / source_width, frame_size[1] / source_height)
        scaled_size = (max(1, round(source_width * scale)), max(1, round(source_height * scale)))
        scaled = pygame.transform.scale(raw, scaled_size)
        x = (frame_size[0] - scaled_size[0]) // 2
        y = frame_size[1] - scaled_size[1]
        frame.blit(scaled, (x, y))
        return frame

    @staticmethod
    def _fallback_frame(frame_size: tuple[int, int], direction: DirectionName, index: int) -> pygame.Surface:
        frame = pygame.Surface(frame_size, pygame.SRCALPHA)
        foot_offset = 4 if index == 1 else -4 if index == 2 else 0
        pygame.draw.ellipse(frame, (236, 214, 178), (12, 2, 24, 24))
        pygame.draw.rect(frame, (66, 95, 143), (14, 26, 20, 30))
        arm_color = COLORS["ink"]
        pygame.draw.line(frame, arm_color, (12, 35), (2, 50), 4)
        pygame.draw.line(frame, arm_color, (36, 35), (46, 50), 4)
        pygame.draw.line(frame, arm_color, (18, 55), (12 + foot_offset, 69), 4)
        pygame.draw.line(frame, arm_color, (30, 55), (36 - foot_offset, 69), 4)
        if direction == "up":
            pygame.draw.line(frame, arm_color, (17, 10), (31, 10), 3)
        elif direction == "left":
            pygame.draw.circle(frame, arm_color, (15, 13), 2)
        elif direction == "right":
            pygame.draw.circle(frame, arm_color, (33, 13), 2)
        else:
            pygame.draw.circle(frame, arm_color, (19, 13), 2)
            pygame.draw.circle(frame, arm_color, (29, 13), 2)
        return frame

    @staticmethod
    def _direction_name(direction: pygame.Vector2) -> DirectionName:
        if abs(direction.x) > abs(direction.y):
            return "right" if direction.x > 0 else "left"
        return "down" if direction.y > 0 else "up"
