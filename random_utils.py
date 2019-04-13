from random import randint

def from_dungeon_level(table, dungeon_level):
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0

# Basic idea  for random choice from dict' and 'random choice index' is this:
# You start with 'random_choice_from_dict', which is a dictionary of values along with their chances.
# Then, you get one of the values based on the chance!

def random_choice_index(chances):
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]

