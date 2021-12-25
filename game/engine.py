# /game/engine.py
from __future__ import annotations

import logging
import random

import tcod

import game.entity
import game.game_map

logger = logging.getLogger(__name__)

class Engine:
    game_map: game.game_map.GameMap
    player: game.entity.Entity
    rng: random.Random

    def handle_enemy_turns(self) -> None:
        logger.info("Enemy turn")
        for it, entity in enumerate(self.game_map.entities - {self.player}):
            logger.info(f"{it} - The {entity.name} wonders when it will get to take a real turn.")


    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view"""
        self.game_map.visible[:] = tcod.map.compute_fov(
            self.game_map.tiles,
            (self.player.x, self.player.y),
            radius=8,
            algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST,
        )
        # If a tile is currently "visible" it will also be marked as "explored".
        self.game_map.explored |= self.game_map.visible
