from game.components.ai import HostileEnemy
from game.components.fighter import Fighter
from game.entity import Actor, Entity

stair_down = Entity(char="v", color=(127, 255, 0), name="Stair Down", blocks_movement=False)
stair_up = Entity(char="^", color=(127, 255, 0), name="Stair Up", blocks_movement=False)

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defence=2, power=5)
)

orc = Actor(
    char="o",
    color=(63,127,0),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defence=0, power=3)
)

troll = Actor(
    char="T",
    color=(0,127,0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defence=1, power=4)
)
