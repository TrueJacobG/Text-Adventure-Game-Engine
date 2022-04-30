from ctypes import POINTER, WinDLL, Structure, sizeof, byref
from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE
from random import uniform
import os


class Game:
    def __init__(self, story):
        self.story = story

    @staticmethod
    def terminal_size():

        LF_FACESIZE = 32
        STD_OUTPUT_HANDLE = -11

        class COORD(Structure):
            _fields_ = [
                ("X", SHORT),
                ("Y", SHORT),
            ]

        class ConsoleFontInfo(Structure):
            _fields_ = [
                ("cbSize", ULONG),
                ("nFont", DWORD),
                ("dwFontSize", COORD),
                ("FontFamily", UINT),
                ("FontWeight", UINT),
                ("FaceName", WCHAR * LF_FACESIZE)
            ]

            @property
            def fields_(self):
                return self._fields_

        kernel32_dll = WinDLL("kernel32.dll")

        get_last_error_func = kernel32_dll.GetLastError
        get_last_error_func.argtypes = []
        get_last_error_func.restype = DWORD

        get_std_handle_func = kernel32_dll.GetStdHandle
        get_std_handle_func.argtypes = [DWORD]
        get_std_handle_func.restype = HANDLE

        get_current_console_font_ex_func = kernel32_dll.GetCurrentConsoleFontEx
        get_current_console_font_ex_func.argtypes = [
            HANDLE, BOOL, POINTER(ConsoleFontInfo)]
        get_current_console_font_ex_func.restype = BOOL

        set_current_console_font_ex_func = kernel32_dll.SetCurrentConsoleFontEx
        set_current_console_font_ex_func.argtypes = [
            HANDLE, BOOL, POINTER(ConsoleFontInfo)]
        set_current_console_font_ex_func.restype = BOOL

        stdout = get_std_handle_func(STD_OUTPUT_HANDLE)

        font = ConsoleFontInfo()
        font.cbSize = sizeof(ConsoleFontInfo)
        res = get_current_console_font_ex_func(stdout, False, byref(font))

        for field_name, _ in font.fields_:
            field_data = getattr(font, field_name)
            font.dwFontSize.X = 10
            font.dwFontSize.Y = 25
            res = set_current_console_font_ex_func(stdout, False, byref(font))

        cmd = 'mode 65, 24'
        os.system(cmd)

    @staticmethod
    def clear_console():
        command = "clear"
        if os.name in ("nt", "dos"):
            command = "cls"
        os.system(command)

    @staticmethod
    def drop_money(enemy_hp):
        return int(enemy_hp * 0.1 * uniform(1.0, 2.0))

    @staticmethod
    def get_information(game, player):
        return game.story[player.currentLocation]['text'], game.story[player.currentLocation]['directions'], \
               game.story[player.currentLocation]['options'], game.story[player.currentLocation]['options_type']

    @staticmethod
    def print_help():
        print("Komendy: ")
        print("help -> Wyswietlenie pomocy")
        print("eq -> Wyswietlenie eq")
        print("skills -> Wyswietlenie umiejetnosci")
        print("quit -> Zapisanie i zamkniecie gry")

        print("\n")

        print(
            "W kazdej lokalizacji mozesz dokonac 4 decyzji. Dokonujesz wyboru poprzez wpisanie odpowiedzi lub podanie numeru (1,2,3,4). Zatwierdzasz wybor klawiszem ENTER.")
        wait = input()

    @staticmethod
    def print_options(option1, option2, option3, option4):
        option1 = " | <" + option1 + "> | "
        option2 = " | <" + option2 + "> | "
        option3 = " | <" + option3 + "> | "
        option4 = " | <" + option4 + "> | "

        filer1 = (64 - (len(option1) + len(option2))) // 2
        filer2 = (64 - (len(option3) + len(option4))) // 2
        filer1 = " " * filer1
        filer2 = " " * filer2

        print("################################################################")
        print(f"{filer1}{option1}{option2}{filer1}")
        print(f"{filer2}{option3}{option4}{filer2}")
        print("################################################################")

    @staticmethod
    def print_screen(text, hp, mana, money, options, currentLocation):
        hp = int(hp)
        Game.clear_console()
        print("Twoja lokalizacja: ", currentLocation)
        print("\033[92m", text, "\033[0m")
        print("\n")
        print(
            f'           \033[91mHP: {hp}/100\033[0m     \033[94mMANA: {mana}/100\033[0m    \033[93mMONEY: {money}\033[0m')
        Game.print_options(*options)

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
