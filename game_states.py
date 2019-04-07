from enum import Enum, auto

# The numbers for the states don't necessarily mean anything.
# In fact, if you're using Python 3.6 or higher, you can use the 'auto' feature to just increment the number for you.

class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    SHOW_INVENTORY = 4
    DROP_INVENTORY = 5
