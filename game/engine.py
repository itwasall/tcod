# /game/engine.py
from __future__ import annotations

import logging
import random

import tcod

import game.entity
import game.game_map
import game.rendering
from game.input_handlers import EventHandler

logger = logging.getLogger(__name__)

class Engine:
    game_map: game.game_map.GameMap
    player: game.entity.Actor
    rng: random.Random

    def __init__(self, player: game.entity.Actor):
        self.event_handler: EventHandler = EventHandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        logger.info("Enemy turn")
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()


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

    def render(self, console: tcod.Console, context: tcod.context.Context) -> None:
        game.rendering.render_map(console, self.game_map)

        console.print(
            x = 1,
            y = 47,
            string = f"HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}"
        )

        context.present(console)

        console.clear()

