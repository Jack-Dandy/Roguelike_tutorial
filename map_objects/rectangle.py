#The __init__ function takes the x and y coordinates of the top left corner,
# and computes the bottom right corner based on the w and h parameters (width and height).
# Used for creating rooms in the dungeon.
class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    # We'll need two additional functions in the Rect class to ensure that two rectangles (rooms) don't overlap.
    # 'center' returns the center coordinate of a given rectangle object.
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)
    # 'intersect' returns 'true' if two given rectangle objects cut into each other someplace, and 'false' if they're seperate.
    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)