import tcod as libtcod
from input_handlers import handle_keys # Importing a function
from components.fighter import Fighter # Import the 'fighter' component
from components.inventory import Inventory # Import the 'inventory' component
from entity import Entity # Importing a class
from fov_functions import initialize_fov , recompute_fov # FoV function
from game_messages import Message, MessageLog
from game_states import GameStates # state enums
from render_functions import clear_all, render_all, RenderOrder # Importing some functions
from map_objects.game_map import GameMap
from entity import Entity, get_blocking_entities_at_location
from death_functions import kill_monster, kill_player



def main():
    # Variables for screen and map size.
    screen_width = 80
    screen_height = 50
    # Health bar variables
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    # Panel variables
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 80
    map_height = 43

    # Some variables used for the dungeon generation algorithm.
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # Variables for Field of Vision for the adventurer.
    fov_algorithm = 0 # '0' is just the default algorithm that libtcod uses; it has more
    fov_light_walls = True # tells us whether or not to 'light up' the walls we see
    fov_radius = 10

    # Variable for deciding on monster & item population on the map.
    max_monsters_per_room = 3
    max_items_per_room = 2

    # Making a dictionary that holds game colors.
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }
    # We use 'int' casting since the libtcod functions require integers, not floats.
    # Creating the entities & components for the game..
    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component)
    entities = [player] # Putting the entities in a list.

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    con = libtcod.console_new(screen_width, screen_height) # Setting up a default console..
    panel = libtcod.console_new(screen_width, panel_height) # Setting up another console, where we'll put stuff like HP and a message log.
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room)
    # Flag for deciding on whether to recompute FoV.
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    # Creating the message log.
    message_log = MessageLog(message_x, message_width, message_height)

    # Setting up user inputs. Keyboard and mouse.
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Setting up a variable that will hold the current game state. player turns, enemy turns, menus, etc..
    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse) # This will record user inputs in the 'key' and 'mouse' variables.
        if fov_recompute: # Check if to recompute FoV.
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width,
                   screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state)

        fov_recompute = False
        libtcod.console_flush() # Print all the last 'put chars' onto the console.

        clear_all(con, entities) # Drawing a blank on the last visited cell.. So there'll be no trail.
        action = handle_keys(key, game_state) # The 'handle_keys' function always returns a dictionary.
        # By using the 'get' function on the 'action' table, we can see if we have one of the related keys.
        # Remember that 'get' gives you the VALUE of the key-value pair.
        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else: # Move player only if he's not blocked by an entity or a wall.
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            else:
                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

        if game_state == GameStates.ENEMY_TURN: # If it's not the player's turn , make every enemy do something , and then switch back to player's turn.
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()