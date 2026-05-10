from __future__ import annotations

from pathlib import Path

import pygame


BASE_DIR = Path(__file__).resolve().parents[1]

WIDTH, HEIGHT = 1280, 640
FPS = 60
WINDOW_TITLE = "人生记忆回廊 - 童年老式琴房"

ROOM_RECT = pygame.Rect(72, 72, 816, 496)
GROWTH_PANEL_RECT = pygame.Rect(WIDTH - 258, 132, 258, 376)
PLAYER_SIZE = (48, 70)
CLUE_SPARK_DURATION = 0.85

COLORS = {
    "ink": (45, 34, 34),
    "shadow": (92, 65, 51),
    "wall": (170, 124, 91),
    "wall_dark": (120, 82, 65),
    "floor_a": (204, 162, 106),
    "floor_b": (194, 148, 92),
    "wood": (111, 70, 42),
    "wood_light": (163, 103, 55),
    "wood_dark": (69, 43, 35),
    "gold": (222, 173, 82),
    "red": (139, 63, 56),
    "red_dark": (92, 44, 48),
    "cream": (244, 222, 176),
    "paper": (252, 236, 200),
    "glass": (128, 190, 204),
    "glass_light": (203, 232, 221),
    "green": (95, 137, 83),
    "blue": (72, 100, 145),
    "amber": (255, 212, 116),
}
