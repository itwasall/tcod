from __future__ import annotations

from typing import Tuple, Optional, TypeVar

T = TypeVar("T", bound=Entity)

import game.game_map


class Entity:
    """A generic object to represent players, enemies, items, etc."""

    gamemap: GameMap

    def __init__(
            self,
            gamemap: Optional[game.game_map.GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocks_movement: bool = True,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        if gamemap:
            # If gamemap isn't provided now then it will be set later
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def spawn(self: T, gamemap: game.game_map.GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at a given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[game.game_map.GameMap] = None) -> None:
        """Place this entity at a new location. Handles moving across GameMaps"""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "gamemap"): # Possibly uninitialised
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)

