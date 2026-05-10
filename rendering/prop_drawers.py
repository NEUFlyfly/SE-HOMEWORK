from __future__ import annotations

import pygame

from core.constants import BASE_DIR, COLORS
from core.models import Furniture


FURNITURE_ASSETS = {
    "bed": "bed.png",
    "cabinet": "cabinet.png",
    "chair": "purple-chair.png",
    "clean_desk": "clean-desk.png",
    "desk": "desk.png",
    "fridge": "fridge.png",
    "little_table": "little-table.png",
    "microwave": "microwave.png",
    "sofa": "red-sofa.png",
}

_asset_cache: dict[tuple[str, tuple[int, int]], pygame.Surface] = {}


def draw_furniture(surface: pygame.Surface, item: Furniture) -> None:
    rect = item.rect
    if item.kind == "piano":
        _draw_piano(surface, rect)
        return

    asset_name = FURNITURE_ASSETS.get(item.kind)
    if asset_name is None:
        return

    asset = _load_scaled_asset(asset_name, rect.size)
    if asset is None:
        _draw_missing_asset(surface, rect)
        return

    surface.blit(asset, rect)


def _load_scaled_asset(asset_name: str, size: tuple[int, int]) -> pygame.Surface | None:
    cache_key = (asset_name, size)
    if cache_key in _asset_cache:
        return _asset_cache[cache_key]

    asset_path = BASE_DIR / "assets" / "furniture" / asset_name
    try:
        image = pygame.image.load(str(asset_path)).convert_alpha()
    except (FileNotFoundError, pygame.error):
        return None

    scaled = pygame.transform.scale(image, size)
    _asset_cache[cache_key] = scaled
    return scaled


def _draw_piano(surface: pygame.Surface, rect: pygame.Rect) -> None:
    pygame.draw.rect(surface, COLORS["wood_dark"], rect.inflate(12, 16), border_radius=6)
    pygame.draw.rect(surface, COLORS["wood"], rect, border_radius=4)
    pygame.draw.rect(surface, COLORS["wood_light"], (rect.x + 14, rect.y + 12, rect.width - 28, 24), border_radius=3)
    pygame.draw.rect(surface, COLORS["paper"], (rect.x + 74, rect.y - 18, 58, 32), border_radius=2)
    pygame.draw.line(surface, COLORS["ink"], (rect.x + 84, rect.y - 8), (rect.x + 120, rect.y - 8), 2)
    pygame.draw.line(surface, COLORS["ink"], (rect.x + 84, rect.y + 2), (rect.x + 126, rect.y + 2), 2)
    pygame.draw.circle(surface, COLORS["amber"], (rect.x + 30, rect.y + 24), 5)

    keys = pygame.Rect(rect.x + 18, rect.y + 48, rect.width - 36, 22)
    pygame.draw.rect(surface, COLORS["cream"], keys)
    for x in range(keys.x + 8, keys.right, 13):
        pygame.draw.rect(surface, COLORS["ink"], (x, keys.y, 6, 14))
    pygame.draw.rect(surface, COLORS["ink"], rect.inflate(12, 16), 3, border_radius=6)


def _draw_missing_asset(surface: pygame.Surface, rect: pygame.Rect) -> None:
    pygame.draw.rect(surface, COLORS["wood_dark"], rect, border_radius=4)
    pygame.draw.rect(surface, COLORS["red"], rect.inflate(-8, -8), border_radius=3)
    pygame.draw.line(surface, COLORS["paper"], rect.topleft, rect.bottomright, 3)
    pygame.draw.line(surface, COLORS["paper"], rect.topright, rect.bottomleft, 3)
