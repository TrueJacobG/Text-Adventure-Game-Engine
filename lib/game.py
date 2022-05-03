from random import uniform


class Game:
    def __init__(self, story):
        self.story = story

    @staticmethod
    def drop_money(enemy_hp: int) -> int:
        return int(enemy_hp * 0.1 * uniform(1.0, 2.0))

    @staticmethod
    def get_information(game, player):
        return game.story[player.currentLocation]['text'], game.story[player.currentLocation]['directions'], \
               game.story[player.currentLocation]['options'], game.story[player.currentLocation]['options_type']

    @staticmethod
    def which_option(decision, options):
        if decision.lower().replace(" ", "") == options[0].lower().replace(" ", "") or decision == str(1):
            return 1
        if decision.lower().replace(" ", "") == options[1].lower().replace(" ", "") or decision == str(2):
            return 2
        if decision.lower().replace(" ", "") == options[2].lower().replace(" ", "") or decision == str(3):
            return 3
        if decision.lower().replace(" ", "") == options[3].lower().replace(" ", "") or decision == str(4):
            return 4
        return None
