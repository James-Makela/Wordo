#!/usr/bin/env python3
"""Guess-My-Word is a game where the player has to guess a word.
Author: James Makela
Company: -
Copyright: 2023

"""
import math
import os
import random
import sys

from rich.console import Console
from os.path import exists
from os import mkdir

console = Console()

# Your code must use PEP8
# Your code must be compatible with Python 3.1x
# You cannot use any libraries outside the python standard library without the explicit permission of your lecturer.

# This code uses terms and symbols adopted from the following source:
# See https://github.com/3b1b/videos/blob/68ca9cfa8cf5a41c965b2015ec8aa5f2aa288f26/_2022/wordle/simulations.py#L104


MISS = 0  # _-.: letter not found ⬜
MISPLACED = 1  # O, ?: letter in wrong place 🟨
EXACT = 2  # X, +: right letter, right place 🟩

MAX_ATTEMPTS = 6
WORD_LENGTH = 5

ALL_WORDS = "./word-bank/all_words.txt"
TARGET_WORDS = "./word-bank/target_words.txt"

STATS_INIT = ["Games played: 0\n",
              "Current streak: 0\n",
              "Max streak: 0\n",
              "Wins: 0\n"
              "1: 0\n",
              "2: 0\n",
              "3: 0\n",
              "4: 0\n",
              "5: 0\n",
              "6: 0\n"]


def play(name):
    """Code that controls the interactive game play"""
    # Initialise stats file if it does not exist

    # select a word of the day:
    word_of_the_day = get_target_word().upper()
    # build a list of valid words (words that can be entered in the UI):
    valid_words = get_valid_words()
    # Keep track of the words entered so far

    keyboard = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    print_list = [" │ │ │ │ "] * MAX_ATTEMPTS
    keymap = [keyboard.index(letter) for letter in "QWERTYUIOPASDFGHJKLZXCVBNM"]

    for i in range(MAX_ATTEMPTS):
        guess = ''
        while guess == '' or guess.startswith("[red"):
            error = ''
            if guess.startswith("[red"):
                error = guess
            output_buffer(print_list, keymap, keyboard, word_of_the_day)

            console.print("Type 'exit' to return to the main menu", justify="center")
            console.print(f" {error} ", justify="center")
            guess = ask_for_guess(valid_words)
        if guess.lower() == "exit":
            return

        guess = guess.upper()
        score = score_guess(guess, word_of_the_day)
        print_list[i] = "│".join(colour_score(guess, score, keyboard))

        if is_correct(score):
            output_buffer(print_list, keymap, keyboard, word_of_the_day)
            console.print(f"Winner! Solved in {i + 1} guesses", justify="center")
            record_stats(True, name, i)
            console.print("Press enter to return to the menu", justify="center")
            input()
            return

    output_buffer(print_list, keymap, keyboard)
    console.print("Try again next time", justify="center")
    console.print(f"The correct word was {word_of_the_day}", justify="center")
    record_stats(False, name)
    console.print("Press enter to return to the menu", justify="center")
    input()
    return True


def is_correct(score):
    """Checks if the score is entirely correct and returns True if it is
    """
    return score == (2,) * 5


def get_valid_words(file_path=ALL_WORDS):
    """returns a list containing all valid words.
    """
    # read words from files and return a list containing all words that can be entered as guesses
    all_words = []
    with open(file_path) as file_handle:
        for word in file_handle:
            all_words.append(word.strip())
    return all_words


def get_target_word(file_path=TARGET_WORDS, seed=None):
    """Picks a random word from a file of words

    Args:
        file_path (str): the path to the file containing the words
        seed (int): used to choose a specific word for testing

    Returns:
        str: a random word from the file
    """
    # read words from a file and return a random word (word of the day)
    words_of_day = []
    with open(file_path) as file_handle:
        for word in file_handle:
            words_of_day.append(word.strip())
    if seed is None:
        choice = random.randint(0, len(words_of_day) + 1)
        return words_of_day[choice]
    return words_of_day[seed]


def ask_for_guess(valid_words, override=None):
    """Requests a guess from the user directly from stdout/in
    Returns:
        str: the guess chosen by the user. Ensures guess is a valid word of correct length in lowercase
    """
    error = "[red on yellow]Invalid word[/]"
    if not override:
        guess_candidate = console.input(f"{' ' * (console.width // 2 - 8)}Guess: ").lower()
    else:
        guess_candidate = override
    if guess_candidate == "exit":
        return guess_candidate
    if guess_candidate not in valid_words:
        return error
    if guess_candidate in valid_words:
        return guess_candidate


def score_guess(guess, target):
    """given two strings of equal length, returns a tuple of ints representing the score of the guess
    against the target word (MISS, MISPLACED, or EXACT)
        """
    target_as_list = list(target)
    discard = []
    result = [MISS] * WORD_LENGTH

    for i, letter in enumerate(guess):
        if letter == target[i]:
            target_as_list.remove(target[i])
            discard.append((target[i], i))
            result[i] = EXACT

    for i, letter in enumerate(guess):
        if letter in target_as_list and (letter, i) not in discard:
            target_as_list.remove(letter)
            result[i] = MISPLACED

    return tuple(result)


def game_help():
    """Provides help for the game"""
    console.clear()
    console.print("Welcome to Wordle\n\n"
                  "Instructions:\n\n"
                  "\t- Guess the correct word in 6 tries or less\n"
                  "\t- Each guess must be a five letter word\n"
                  "\t- As you make guesses the colours of the\n"
                  "\t  letters will change to indicate how your\n"
                  "\t  guess compares to the word of the day\n\n"
                  "Some examples:\n\n"
                  "┌─┬─┬─┬─┬─┐\n"
                  "│P│E│A│R│[bold black on #6aaa64]S[/]│\n"
                  "└─┴─┴─┴─┴─┘\n"
                  "\t- Here the S is in the correct place\n\n"
                  "┌─┬─┬─┬─┬─┐\n"
                  "│A│P│P│[bold black on #d1b036]L[/]│E│\n"
                  "└─┴─┴─┴─┴─┘\n"
                  "\t- Here the L is in the target word,\n"
                  "\t  but not in the correct spot\n\n"
                  "┌─┬─┬─┬─┬─┐\n"
                  "│G│R│A│P│E│\n"
                  "└─┴─┴─┴─┴─┘\n"
                  "\t- Here no letters are correct\n\n"
                  "Press enter to go back to the main menu"
                  )
    input()


def colour_score(guess, score, keyboard=None):
    if keyboard is None:
        keyboard = ['']*26
    print_item = []
    style = ""
    for i, letter in enumerate(guess):
        if score[i] == 0:
            style = "white on #666666"
            if "bold" not in keyboard[ord(letter) - ord("A")]:
                keyboard[ord(letter) - ord("A")] = " "
        elif score[i] == 1:
            style = "bold black on #d1b036"
            if "bold" not in keyboard[ord(letter) - ord("A")]:
                keyboard[ord(letter) - ord("A")] = f"[{style}]{letter}[/]"
        elif score[i] == 2:
            style = "bold black on #6aaa64"
            keyboard[ord(letter) - ord("A")] = f"[{style}]{letter}[/]"

        print_item.append(f"[{style}]{guess[i]}[/]")
    return print_item


def output_buffer(print_list, keymap, keyboard, word_of_day=""):
    console.clear()
    console.print("< WORDO >", justify="center")
    console.print("┌─┬─┬─┬─┬─┐", justify="center")
    for i, item in enumerate(print_list):
        console.print(f"│{item}│", justify="center")

        if i <= len(print_list) - 2:
            console.print("├─┼─┼─┼─┼─┤", justify="center")
    console.print("└─┴─┴─┴─┴─┘", justify="center")

    print_keyboard = []
    for number in keymap:
        print_keyboard.append(keyboard[number])

    console.print("".join(print_keyboard[:10]), justify="center")
    console.print(f" {''.join(print_keyboard[10:19])}", justify="center")
    console.print(f"  {''.join(print_keyboard[19:])}\n", justify="center")


def main_menu():

    name = init_stats()
    while True:
        console.clear()

        console.print(
            "Welcome to Wordo, the word guessing game.\n"
            "Guess the 5 letter word in 6 tries or less.\n\n"
            "|  1 - Play Game       |\n"
            "|  2 - View Stats      |\n"
            "|  3 - View Help       |\n"
            "|  4 - User Management |\n"
            "|  5 - Quit            |\n", justify="center")
        match input():
            case "1":
                play(name)
            case "2":
                view_stats(name)
            case "3":
                game_help()
            case "4":
                user_menu()
            case "5":
                console.clear()
                sys.exit()


def user_menu():
    while True:
        console.clear()

        console.print(
            "User Menu\n\n"
            "|  1 - Change User     |\n"
            "|  2 - Add user        |\n"
            "|  3 - Remove User     |\n", justify="center")

        match input():
            case "1":
                main_menu()
            case "2":
                main_menu()
            case "3":
                delete_user()


def delete_user():
    console.clear()
    console.print("Please Select a name to delete", justify="center")
    names = display_names()
    choice = input()
    name = names[int(choice) - 1]
    try:
        names.remove(name)
        os.remove(f"./stats/{name}")
    except (IndexError, ValueError):
        return
    # Next we need to remove the name from the names file then we need to remove the user file for that name
    with open("./stats/names", "w") as file:
        for name in names:
            file.writelines(name)
        file.writelines("\n")


def init_stats():
    if not exists("./stats/"):
        mkdir("./stats/")

    names = []
    console.clear()
    console.print("Please Select a name, or enter a new name", justify="center")
    if exists("./stats/names"):
        names = display_names()

        user_name = None
        while user_name is None:
            choice = input()
            if choice == "":
                choice = "1"
            try:
                user_name = names[int(choice)-1]
            except (IndexError,  ValueError):
                user_name = choice

    else:
        console.clear()
        console.print("Please enter your name to begin.")
        user_name = console.input(f"{' ' * (console.width // 2 - 8)}Name: ").upper()

    with open("./stats/names", "a") as names_file:
        if user_name not in names:
            names_file.writelines(f"{user_name.lower()}\n")

    if not exists(f"./stats/{user_name}"):
        with open(f"./stats/{user_name}", "w") as stats:
            stats.writelines(STATS_INIT)

    return user_name


def display_names():
    names = []
    if exists("./stats/names"):
        with open("./stats/names", "r") as names_file:
            for line in names_file:
                if len(line) > 1:
                    names.append(line.strip())

        for i, name in enumerate(names):
            console.print(f"{i + 1}. {name.upper()}", justify="center")
    return names


def record_stats(win, name, tries=0):
    strings = []
    with open(f"./stats/{name}") as stats:
        lines = make_dict(stats)

    if win:
        lines["Games played"] += 1
        lines["Current streak"] += 1
        lines["Wins"] += 1
        if lines["Current streak"] > lines["Max streak"]:
            lines["Max streak"] = lines["Current streak"]
        lines[str(tries + 1)] += 1
    else:
        lines["Games played"] += 1
        lines["Current streak"] = 0

    # convert the dictionary back to a list of lines
    for key, value in lines.items():
        strings.append(f"{key}: {str(value)}\n")

    with open(f"./stats/{name}", "w") as stats:
        stats.writelines(strings)


def make_dict(stats):
    lines = {}
    for line in stats:
        line = line.split(":")
        lines[line[0]] = int(line[1])
    return lines


def view_stats(user_name):
    console.clear()

    with open(f"./stats/{user_name}") as stats:
        lines = make_dict(stats)

    console.clear()
    console.print(user_name.upper(), justify="center")
    wins = int(lines["Wins"])
    if wins != 0:
        console.print(f"Games played: {lines['Games played']}\n"
                      f"Current streak: {lines['Current streak']}\n"
                      f"Max streak: {lines['Max streak']}\n"
                      f"Win %: {round(wins / int(lines['Games played']) * 100)}\n"
                      f"Guess Distribution:\n"
                      f"1: [#6aaa64]{math.ceil(int(lines['1']) / wins * 50) * '❚'}\n[/]"
                      f"2: [#6aaa64]{math.ceil(int(lines['2']) / wins * 50) * '❚'}\n[/]"
                      f"3: [#6aaa64]{math.ceil(int(lines['3']) / wins * 50) * '❚'}\n[/]"
                      f"4: [#6aaa64]{math.ceil(int(lines['4']) / wins * 50) * '❚'}\n[/]"
                      f"5: [#6aaa64]{math.ceil(int(lines['5']) / wins * 50) * '❚'}\n[/]"
                      f"6: [#6aaa64]{math.ceil(int(lines['6']) / wins * 50) * '❚'}\n[/]")
    else:
        console.print("No wins yet")

    console.print("Press enter to go back to the menu")
    input()
    return


def main():
    main_menu()


if __name__ == "__main__":
    main()
