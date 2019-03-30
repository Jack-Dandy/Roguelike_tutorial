import tcod as libtcod
from input_handlers import handle_keys # Importing a function
from entity import Entity # Importing a class
from render_functions import clear_all, render_all # Importing some functions
from map_objects.game_map import GameMap

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    # Making a dictionary that holds game colors.
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }
    # We use 'int' casting since the libtcod functions require integers, not floats.
    # Creating the entities for the game..
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [npc, player] # Putting the entities in a list.

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    con = libtcod.console_new(screen_width, screen_height) # Setting up a default console..
    game_map = GameMap(map_width, map_height)
    # Setting up user inputs. Keyboard and mouse.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse) # This will record user inputs in the 'key' and 'mouse' variables.
        render_all(con, entities, game_map, screen_width, screen_height, colors)
        libtcod.console_flush() # Print all the last 'put chars' onto the console.

        clear_all(con, entities) # Drawing a blank on the last visited cell.. So there'll be no trail.
        action = handle_keys(key) # The 'handle_keys' function always returns a dictionary.
        # By using the 'get' function on the 'action' table, we can see if we have one of the related keys.
        # Remember that 'get' gives you the VALUE of the key-value pair.
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy): # Move player only if he's not blocked.
                player.move(dx, dy)
        if exit:
            return True
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()