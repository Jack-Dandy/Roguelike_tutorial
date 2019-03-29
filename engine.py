import tcod as libtcod
from input_handlers import handle_keys

def main():
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2) # We use 'int' casting since the libtcod functions require integers, not floats.
    player_y = int(screen_height / 2)

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    con = libtcod.console_new(screen_width, screen_height) # Setting up a default console..

    # Setting up user inputs. Keyboard and mouse.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse) # This will record user inputs in the 'key' and 'mouse' variables.
        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_flush() # Print all the last 'put chars' onto the console.

        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE) # Drawing a blank on the last visited cell.. So there'll be no trail.
        action = handle_keys(key) # The 'handle_keys' function always returns a dictionary.
        # By using the 'get' function on the 'action' table, we can see if we have one of the related keys.
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy
        if exit:
            return True
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()