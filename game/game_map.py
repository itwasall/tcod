# /game/game_map.py
from __future__ import annotations

from typing import Iterator, Optional, TYPE_CHECKING, Set

import numpy as np

import game.engine
from game.entity import Actor

if TYPE_CHECKING:
    from game.entity import Entity


class GameMap:
    def __init__(
        self, 
        engine: game.engine.Engine, 
        width: int, 
        height: int
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.tiles = np.zeros((width, height), dtype=np.uint8, order="F")
        self.entities: Set[game.entity.Entity] = set()
        self.enter_xy = (width // 2, height // 2)  # Entrance coordinates

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

    def get_blocking_entity_at(self, x: int, y: int) -> Optional[game.entity.Entity]:
        """Returns an entity that blocks the position at x,y if one exists, otherwise returns None"""
        for entity in self.entities:
            if entity.blocks_movement and entity.x == x and entity.y == y:
                return entity
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterates over this maps living actors"""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None
