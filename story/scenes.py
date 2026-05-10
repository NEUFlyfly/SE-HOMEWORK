from __future__ import annotations

from collections.abc import Callable

from core.models import SceneData
from story.scene_01_childhood import childhood_piano_room
from story.scene_02 import scene_02
from story.scene_03 import scene_03
from story.scene_04 import scene_04

SceneFactory = Callable[[], SceneData]

DEFAULT_SCENE_ID = "childhood_piano_room"
SCENE_FACTORIES: dict[str, SceneFactory] = {
    "childhood_piano_room": childhood_piano_room,
    "scene_02": scene_02,
    "scene_03": scene_03,
    "scene_04": scene_04,
}


def get_scene(scene_id: str) -> SceneData:
    return SCENE_FACTORIES[scene_id]()


def all_scenes() -> tuple[SceneData, ...]:
    return tuple(factory() for factory in SCENE_FACTORIES.values())
