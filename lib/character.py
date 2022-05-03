import json
from os import path
import os
from random import randint
import sys
from time import sleep

from typing import Union

from .game import Game
from .enemy import Enemy
from .console import *


class Character:
    def __init__(self):
        if not path.isfile("character.json"):
            with open("models/character_model.json") as f:
                character = json.load(f)

            with open("character.json", "w") as f:
                json.dump(character, f)

            name, clas, weapon, armor, difficulty = self.play_intro()
            self.name: str = name
            self.clas: str = clas
            self.difficulty: int = difficulty

            self.eq: dict[str, dict[str, list[int]]] = {
                "weapons": weapon,
                "armors": armor
            }

        else:
            with open("character.json") as f:
                character = json.load(f)

            self.name: str = character['name']
            self.clas: str = character['clas']
            self.eq: dict[str, dict[str, list[int]]] = character['eq']
            self.difficulty: float = 0.5

        with open("models/attacks.json") as f:
            attacks = json.load(f)
            self.attacks = attacks[self.clas]

        self.hp: float = character['hp']
        self.mana: float = character['mana']
        self.money: int = character['money']
        self.currentLocation: str = character['current_location']
        self.seenFightingLocation: list[str] = character['seenFightingLocation']

    @staticmethod
    def play_intro() -> (str, str, dict[str, list[int]], dict[str, list[int]], float):
        print("Witaj! Musisz stworzyc swoja postac!")
        print("Podaj swoje imie poszukiwaczu przygod: ")
        name: str = input()
        print("Podaj poziom trudnosci: <1> <2> <3>")
        print("1. Latwy 2. Normalny 3. Trudny")
        difficulty: float = input()
        if difficulty == 1:
            difficulty = 0.5
        elif difficulty == 2:
            difficulty = 1
        elif difficulty == 3:
            difficulty = 1.2

        print("Wybierz klase: ")
        clas: str = input("1. <Wojownik> 2. <Lucznik> 3. <Mag>\n\n")
        if clas == str(1) or clas.lower() == "wojownik":
            clas: str = "Wojownik"
            weapon: dict[str, list[int]] = {"Zwykly miecz": [80, 10]}
            armor: dict[str, list[int]] = {"Zwykla tarcza": [80, 10]}
        elif clas == str(2) or clas.lower() == "lucznik":
            clas: str = "Lucznik"
            weapon: dict[str, list[int]] = {"Zwykly luk": [80, 10]}
            armor: dict[str, list[int]] = {"Dziwny naszyjnik": [80, 10]}
        else:
            clas: str = "Mag"
            weapon: dict[str, list[int]] = {"Stara rozdzka": [80, 10]}
            armor: dict[str, list[int]] = {"Slomiany kapelusz": [80, 10]}

        print("\n Swietnie! Decyzje dokonujesz poprzez wpisanie odpowiedniego wyboru lub numeru. Jesli chcesz zamknac gre wpisz QUIT. Pomoc -> help")

        wait: any = input()

        return name, clas, weapon, armor, difficulty

    def save_character(self):
        with open("character.json") as f:
            character = json.load(f)

        character['name']: str = self.name
        character['clas']: str = self.clas
        character['hp']: float = self.hp
        character['mana']: float = self.mana
        character['money']: int = self.money
        character['current_location']: str = self.currentLocation
        character['seenFightingLocation']: list[str] = self.seenFightingLocation
        character['eq']: dict[str, dict[str, list[int]]] = self.eq

        with open("character.json", "w") as f:
            json.dump(character, f)

    @staticmethod
    def delete_character():
        print("UMARLES! (Twoja postac zostanie usunieta za chwile)")
        wait: any = input()
        os.remove("character.json")
        sleep(1)
        sys.exit(1)

    def print_eq(self):
        print("W twoim plecaku znajduja sie: \n")
        weapons: list[list[str]] = []
        armors: list[list[str]] = []

        for weaponType in self.eq.items():
            if weaponType[0] == "weapons":
                weapons.append(list(weaponType[1].items()))
            else:
                armors.append(list(weaponType[1].items()))

        nr = 0
        printc("Bronie:", "blue")
        for item in weapons[0]:
            nr += 1
            printc(f"{nr}. {item[0]}", "yellow")
            printc("Att/Obr: {item[1][0]} Wyt: {item[1][1]}")

        nr = 0
        printc("Zbroje:", "blue")
        for item in armors[0]:
            nr += 1
            printc(f"{nr}. {item[0]}", "blue")
            printc("Att/Obr: {item[1][0]} Wyt: {item[1][1]}")

        print("\nChcesz zmienic swoja glowna bron i zbroje?")
        print("<TAK> <NIE>")
        decision: str = input()
        if decision.lower() == "tak" or decision == str(1):
            self.rearrange_eq(weapons[0], armors[0])
        return

    def fight(self, current_location, difficulty, game):
        enemy: Enemy = Enemy(current_location, difficulty, game.story)
        coins_for_fight = enemy.hp
        defense = self.hp // 14 * self.difficulty
        while True:
            # enemy turn
            random_number = randint(0, 3)
            text = "\033[91m" + "ENEMY HP: " + str(enemy.hp) + "\n\n" + \
                   enemy.attacksDescription[random_number] + "\033[0m"
            if defense >= enemy.attacksDMG[random_number]:
                enemy.hp -= enemy.hp // 5
                self.mana += 10
                if self.mana > 100:
                    self.mana = 100
                    print("Odbiles atak wroga!")
                else:
                    print("Odbiles atak wroga i twoja mana ulegla regeneracji!")
            else:
                self.hp -= enemy.attacksDMG[random_number] - defense
                if self.hp <= 0:
                    self.delete_character()
            options = self.attacks
            Game.print_screen(text, self.hp,
                              self.mana, self.money, options, self.currentLocation)
            # player turn
            at = input()
            defense = self.attack(at, enemy, game.story)
            if defense is None:
                return None

            if enemy.hp <= 0:
                print(enemy.defeated)
                self.money += Game.drop_money(coins_for_fight)
                coins_for_fight = "\033[93m" + str(coins_for_fight) + "\033[0m"
                print("Za udana walke otrzymujesz ",
                      coins_for_fight, " pieniedzy!")
                wait = input()
                break

            text = enemy.getDMG[random_number]
            print(text)
            wait = input()
        return 13

    def attack(self, at, enemy, story):
        defense = 0
        dmg = 0
        weapon_destruction_damage = 0

        which_attack = Game.which_option(at, self.attacks)
        weapons = []
        armors = []
        for weaponType in self.eq.items():
            if weaponType[0] == "weapons":
                weapons.append(list(weaponType[1].items()))
            else:
                armors.append(list(weaponType[1].items()))

        try:
            weapon = list(weapons[0][0])
            armor = list(armors[0][0])
        except:
            Game.clear_console()
            print("Nie masz broni lub zbroi! Twoj przeciwnik Cie nokaltuje i okrada!")
            self.money -= self.money // 2
            print(
                "Zostajesz odnaleziony przez innego poszukiwacza. Przedstawil Ci sie jako Linus. Odprowadza Cie do szpitala w Eagle Town.")
            wait = input()
            return None

        weapon_name = list(self.eq["weapons"].keys())[0]
        armor_name = list(self.eq["armors"].keys())[0]

        if which_attack == 1:
            dmg = 1
            weapon_destruction_damage = 1

        if which_attack == 2:
            dmg = 1.5
            weapon_destruction_damage = 2

        enemy.hp -= weapon[1][0] * dmg
        self.eq["weapons"][weapon_name][1] -= weapon_destruction_damage

        if self.eq["weapons"][weapon_name][1] <= 0:
            del self.eq["weapons"][weapon_name]
            print("Twoja bron ulegla zniszczeniu!")
            wait = input()

        if which_attack == 3:
            if self.clas == "Wojownik":
                addDef = 15
            elif self.clas == "Lucznik":
                addDef = 10
            else:
                addDef = 5

            defense = addDef + armor[1][0] // 4

            self.eq["armors"][armor_name][1] -= 1

            if self.eq["armors"][armor_name][1] <= 0:
                del self.eq["armors"][armor_name]
                print("TWoja zbroja ulegla zniszczeniu!")
                wait = input()

        if which_attack == 4:
            if self.clas == "Mag":
                addHeal = 15
            elif self.clas == "Lucznik":
                addHeal = 10
            else:
                addHeal = 5
            self.hp += addHeal + armor[1][0] // 4

        return defense

    def make_move(self, decision, options, options_type, directions, game):
        op = (Game.which_option(decision, options)) - 1
        if options_type[op] == "move":
            self.currentLocation = directions[op]
        if options_type[op] == "eq":
            self.print_eq()
        if options_type[op] == "shop":
            self.shop(op, game)

    def mana_regeneration(self):
        random_number = randint(10, 22)
        if self.clas == "Mag":
            class_multiplication = 2
        elif self.clas == "Lucznik":
            class_multiplication = 1
        else:
            class_multiplication = 0.5
        self.mana += int(random_number * class_multiplication)
        if self.mana > 100:
            self.mana = 100

    def skills(self):
        opt = ["Leczenie", "Ulepszenie Broni",
               "Wytworzenie monet", "Gambling", "Storzenie broni *rare*"]
        print("Twoje umiejetnosci: ")
        print("1. ", opt[0])
        print("2. ", opt[1])
        print("3. ", opt[2])
        print("4. ", opt[3])
        print("5. ", opt[4])
        print("\nCo chcesz zrobic?")

        try:
            dec = (Game.which_option(input(), opt)) - 1
        except:
            return

        if dec is None:
            return

        random_number = randint(5, 20)
        self.mana -= 25
        if self.mana < 0:
            self.mana += 25
            print("Masz za malo many!")
            wait = input()
            return

        if dec == 0:
            if self.hp > 100:
                print("Nie mozesz uleczyc sie ponad 100 HP.")
                wait = input()
                return
            self.hp += random_number
            if self.hp > 100:
                self.hp = 100
            print("Zostales uleczony i twoje zdrowie wynosi ", self.hp)
            wait = input()
            return

        if dec == 1:
            for item in self.eq.items():
                self.eq[item[0]][0] += random_number // 4
                self.eq[item[0]][1] += random_number // 4

            print("Ulepszyles i naprawiles swoja bron")
            wait = input()
            return
        if dec == 2:
            self.money += random_number
            print("Udalo ci sie wyczarowac ", random_number, " monet!")
            wait = input()
            return

        if dec == 3:
            print(
                "Rzucasz moneta! Jesli wypadnie reszka wygrywasz pieniadze, jesli nie to tracisz czesc swojej fortuny!")
            self.mana += 25
            if self.money < 10:
                print("Masz za malo pieniedzy!")
                wait = input()
                return
            if randint(0, 1) == 0:
                print("Nie udalo ci sie wygrac!")
                self.money -= 10
                wait = input()
                return

            coins = self.money // 12 + randint(5, 20)
            print(f"Brawo wygrales \033[93m{coins}\033[0m monet!")
            wait = input()
            return

        if dec == 4:
            print("Nie udalo ci sie. Jestes jeszcze za slaby!")
            wait = input()
            return

    def shop(self, op, GAME):
        which_shelf = GAME.story[self.currentLocation]["directions"][op]
        shelf = GAME.story[self.currentLocation]["shop"][which_shelf][self.clas]
        for item in shelf.items():
            print(item[0], " --- ", "\033[91mAtt/Obr: ", item[1][0],
                  "\033[0m\033[95mWyt: ", item[1][1], "\033[0m\033[93mCena: ", item[1][2], "\033[0m")

        print("Na co masz ochote?")
        decision = input()
        try:
            decision = (Game.which_option(decision, list(shelf.keys()))) - 1
        except:
            return

        bought_item_name = list(shelf)[decision]
        bought_item_stats = shelf[bought_item_name]
        if self.money < bought_item_stats[2]:
            print("Nie masz wystarczajaco pieniedzy! Wynocha z mojego sklepu!")
            wait = input()
            return
        if bought_item_name in self.eq:
            print("Juz posiadasz taki przedmiot!")
            wait = input()
            return
        self.money -= bought_item_stats[2]
        self.eq[which_shelf][bought_item_name] = bought_item_stats[0:2]
        print("Dziekuje za dokonanie u mnie zakupu :D")
        wait = input()

    def rearrange_eq(self, weapons, armors):

        print("Ktora bron chcesz ustawic jako glowna? (podaj numer)")
        try:
            weaponDecision = int(input()) - 1
        except:
            weaponDecision = 1
        print("Ktora zbroje chcesz ustawic jako glowna? (podaj numer)")
        try:
            armorDecision = int(input()) - 1
        except:
            armorDecision = 1

        try:
            self.eq["weapons"] = self.move_element_in_dict(
                self.eq["weapons"], weapons[weaponDecision][0])

            self.eq["armors"] = self.move_element_in_dict(
                self.eq["armors"], armors[armorDecision][0])
        except:
            print("Podales zly numer!")
            wait = input()

        self.print_eq()

    @staticmethod
    def move_element_in_dict(di, key):
        queue = []
        result = {}
        for item in di.items():
            if item[0] == key:
                result[item[0]] = item[1]
                continue
            queue.append(item)

        for item in queue:
            result[item[0]] = item[1]

        return result
