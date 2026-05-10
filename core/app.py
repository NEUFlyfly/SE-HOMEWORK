from __future__ import annotations

try:
    import pygame
except ImportError:  # pragma: no cover - only used when pygame is absent locally.
    print("未安装 pygame。请先运行：python -m pip install pygame")
    raise

from core.constants import FPS, HEIGHT, WIDTH, WINDOW_TITLE
from core.scene import StoryRoomScene
from core.scene_manager import SceneManager
from story.scenes import childhood_piano_room


def _initial_window_size() -> tuple[int, int]:
    display = pygame.display.Info()
    screen_width = display.current_w or WIDTH
    screen_height = display.current_h or HEIGHT
    usable_width = max(640, int(screen_width * 0.92))
    usable_height = max(360, int(screen_height * 0.88))
    aspect = WIDTH / HEIGHT

    window_width = usable_width
    window_height = round(window_width / aspect)
    if window_height > usable_height:
        window_height = usable_height
        window_width = round(window_height * aspect)
    return window_width, window_height


def run() -> int:
    pygame.init()
    try:
        pygame.display.set_caption(WINDOW_TITLE)
        screen = pygame.display.set_mode(_initial_window_size(), pygame.RESIZABLE)
        clock = pygame.time.Clock()
        scene_manager = SceneManager(StoryRoomScene(childhood_piano_room()))

        while scene_manager.running:
            dt = clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((max(640, event.w), max(360, event.h)), pygame.RESIZABLE)
                if not scene_manager.handle_event(event):
                    break
            if not scene_manager.running:
                break
            scene_manager.update(dt)
            scene_manager.draw(screen)
            pygame.display.flip()
    finally:
        pygame.quit()
    return 0
