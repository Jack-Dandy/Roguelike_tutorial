from enum import Enum, auto

# The numbers for the states don't necessarily mean anything.
# In fact, if you're using Python 3.6 or higher, you can use the 'auto' feature to just increment the number for you.

class GameStates(Enum):
    PLAYERS_TURN = auto()
    ENEMY_TURN = auto()

