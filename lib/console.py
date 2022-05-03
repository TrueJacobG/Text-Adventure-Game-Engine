from typing import Optional

from ctypes import POINTER, WinDLL, Structure, sizeof, byref
from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE
import os


def printc(text: str, color: Optional[str]) -> None:
    if color.lower() == "red":
        print("\033[91m" + text + "\033[0m")
    if color.lower() == "blue":
        print("\033[94m" + text + "\033[0m")
    if color.lower() == "green":
        print("\033[92m" + text + "\033[0m")
    if color.lower() == "yellow":
        print("\033[93m" + text + "\033[0m")
    if color.lower() == "cream":
        print("\033[95m" + text + "\033[0m")
    if color.lower() == "lblue":
        print("\033[96m" + text + "\033[0m")
    else:
        print(text)


def terminal_size():
    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(Structure):
        _fields_ = [("X", SHORT),("Y", SHORT),]

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


def print_help():
    print("Komendy: ")
    print("help -> Wyswietlenie pomocy")
    print("eq -> Wyswietlenie eq")
    print("skills -> Wyswietlenie umiejetnosci")
    print("quit -> Zapisanie i zamkniecie gry")

    print("\n")

    print("W kazdej lokalizacji mozesz dokonac 4 decyzji. Dokonujesz wyboru poprzez wpisanie odpowiedzi lub podanie numeru (1,2,3,4). Zatwierdzasz wybor klawiszem ENTER.")
    wait = input()


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


def print_screen(text, hp, mana, money, options, current_location):
    hp = int(hp)
    clear_console()
    print("Twoja lokalizacja: ", current_location)
    print("\033[92m", text, "\033[0m")
    print("\n")
    print(
        f'           \033[91mHP: {hp}/100\033[0m     \033[94mMANA: {mana}/100\033[0m    \033[93mMONEY: {money}\033[0m')
    print_options(*options)


def clear_console():
    command: str = "clear"
    if os.name in ("nt", "dos"):
        command: str = "cls"
    os.system(command)
