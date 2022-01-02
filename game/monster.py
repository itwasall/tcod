from typing import Tuple

from entity import Entity
import game.game_map

class Breed:
    def __init__(
            self,
            breed_name: str,
            base_health: int,
            base_attack: int,
            base_defence: int,
            base_health_recovery: int
    ):
        self.breed_name = breed_name

        self.base_health = base_health,
        self.base_health_recovery = base_health_recovery
        self.base_attack = base_attack
        self.base_defence = base_defence

        self.current_health = base_health
        self.current_attack = base_attack
        self.current_defence = base_defence

        self.equipment = {}
        self.attacks = {}

class Monster(Entity):
    def __init__(
            self,
            gamemap: game.game_map.GameMap,
            x: int,
            y: int,
            char: str,
            color: Tuple[int, int, int],
            breed: Breed,
            blocks_movement: bool = True,
    ):
        super().__init__(gamemap, x, y, char, color, breed.breed_name, blocks_movement)

Goblin_Breed = Breed('Goblin', 100, 30, 20, 4)
