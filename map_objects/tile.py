# This file is used to define the 'tiles' that make up the dungeon map!

class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, block_sight=None): # Note the default parameter for block_sight..
        self.blocked = blocked # if it's blocked, you can't move through it

        # By default, if a tile is blocked, it also blocks sight. But they're not necessarily identical.
        # For example, a lava pit can block you from moving, but you can SEE through it.
        # And you can't see through a dark room, but you can MOVE through it.
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight