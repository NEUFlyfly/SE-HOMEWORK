from __future__ import annotations

from core.models import Interaction


class DialogueState:
    def __init__(self, initial_text: str) -> None:
        self.text = initial_text
        self.progress: dict[str, int] = {}
        self.owner: str | None = None

    def advance(self, interaction: Interaction) -> None:
        line_index = self.progress.get(interaction.name, 0)
        self.text = interaction.lines[line_index % len(interaction.lines)]
        self.progress[interaction.name] = line_index + 1
        self.owner = interaction.name

    def set_ambient(self, text: str) -> None:
        self.text = text
        self.owner = None
