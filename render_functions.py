# This file will hold our functions for drawing and clearing from the screen.
import libtcodpy as libtcod


def render_all(con, entities, game_map, screen_width, screen_height, colors):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    # Draw all entities in the list, using the 'draw_entity' function.
    for entity in entities:
        draw_entity(con, entity)

    # I guess console-blit copies stuff from the first parameter ccnsole into the root console.
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    # 'clear_all' is what we'll use to clear all the entities after drawing them to the screen. It's just a loop that calls another function.
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity):
    # Draw things, using the entity's values.
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)