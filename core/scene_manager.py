from __future__ import annotations

import pygame

from core.scene import StoryRoomScene


class SceneManager:
    def __init__(self, initial_scene: StoryRoomScene) -> None:
        self.current_scene = initial_scene
        self.running = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        self.running = self.current_scene.handle_event(event)
        return self.running

    def update(self, dt: float) -> None:
        self.current_scene.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        self.current_scene.draw(screen)
