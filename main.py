import json

import sys
from time import sleep

from lib import Game
from lib import Character


# twitter.com/TrueJacobG

def play(player, game_obj):
    # variables
    text, directions, options, options_type = Game.get_information(game_obj, player)

    if game_obj.story[player.currentLocation][
        "fightingLocation"] and player.currentLocation not in player.seenFightingLocation:

        player.mana_regeneration()

        text1 = game_obj.story[player.currentLocation]['text1']
        print(text1)
        while True:
            state = player.fight(player.currentLocation,
                                 player.difficulty, game_obj)
            player.seenFightingLocation.append(player.currentLocation)
            if state is None:
                player.currentLocation = "EAGLE TOWN"
            text, directions, options, options_type = Game.get_information(
                game_obj, player)
            break

    Game.print_screen(text, player.hp,
                      player.mana, player.money, options, player.currentLocation)

    decision = input()
    flag = True
    while flag:
        if decision.lower() == "quit":
            player.save_character()
            Game.clear_console()
            print("Do zobaczenia niedługo :D")
            sleep(1)
            Game.clear_console()
            flag = False
            sys.exit()
        if decision.lower() == "help":
            Game.print_help()
            print("Co chcesz zrobić?")
            decision = input()
            continue
        if decision.lower() == "skills":
            player.skills()
            print("Uzyles umiejetnosci! Gdzie chcesz teraz isc?")
            decision = input()
            continue
        if Game.which_option(decision, options) is None:
            print("Nie rozumiem cie...")
            decision = input()
            continue

        player.make_move(decision, options, options_type, directions, game_obj)
        flag = False


def main():
    Game.terminal_size()

    with open("story.json") as f:
        story = json.load(f)

    player = Character()
    player.save_character()
    game_obj = Game(story)

    while True:
        play(player, game_obj)


if __name__ == '__main__':
    main()
