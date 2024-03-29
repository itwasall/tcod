# /game/actions.py
from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    import game.engine
    import game.entity


class Action:
    def __init__(self, entity: game.entity.Actor) -> None:
        super().__init__()
        self.entity = entity  # The object performing the action.
    
    @property
    def engine(self) -> game.engine.Engine:
        """Returns the engine this action belongs to"""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action now.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit

class Wait(Action):
    def perform(self) -> None:
        pass


class ActionWithDirection(Action):
    def __init__(self, entity: game.entity.Actor, dx: int, dy: int):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination"""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[game.entity.Actor]:
        """Returns the blocking entity at this actions destination"""
        return self.engine.game_map.get_blocking_entity_at(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[game.entity.Actor]:
        """Returns the actor at this actions destination"""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError


class Move(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles[dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        self.entity.x, self.entity.y = dest_x, dest_y

class Melee(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            return # No entity to attack

        damage = self.entity.fighter.power - target.fighter.defence

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if damage > 0:
            print(f"{attack_desc} for {damage} hit points.")
            target.fighter.hp -= damage
        else:
            print(f"{attack_desc} but does no damage")


class Bump(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return Melee(self.entity, self.dx, self.dy).perform()
        else:
            return Move(self.entity, self.dx, self.dy).perform()