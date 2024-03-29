import copy
from typing import TYPE_CHECKING
import tcod
import logging
import random
import game.engine
import game.procgen
import game.input_handlers
import game.entity_factories

WIDTH, HEIGHT = int(1920/2), 1080
FLAGS = tcod.context.SDL_WINDOW_RESIZABLE | tcod.context.SDL_WINDOW_MAXIMIZED


def main() -> None:
    screen_width = 100
    screen_height = 50

    map_width = 100
    map_height = 50

    room_max_size = 20
    room_min_size = 5
    max_rooms = 30
    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet("data/dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    player = copy.deepcopy(game.entity_factories.player)

    engine = game.engine.Engine(player)
    engine.rng = random.Random()
    engine.game_map = game.procgen.generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine,
    )
    # engine.player = game.entity.Entity(engine.game_map, *engine.game_map.enter_xy, "@", (255, 255, 255), name="Player")
    engine.player = game.entity_factories.player.spawn(engine.game_map, *engine.game_map.enter_xy)
    engine.update_fov()

    event_handler = game.input_handlers.EventHandler(engine)

    with tcod.context.new(
            width=WIDTH,
            height=HEIGHT,
            columns=screen_width,
            rows=screen_height,
            tileset=tileset,
            title="Test",
            sdl_window_flags=FLAGS,
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(root_console, context)
            #root_console.clear()
            #event_handler.on_render(console=root_console)
            #context.present(root_console)

            for event in tcod.event.wait():
                event_handler = event_handler.handle_events(event)
            


if __name__ == "__main__":
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    main()
