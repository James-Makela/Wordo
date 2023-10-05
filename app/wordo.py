#!/usr/bin/env python3
import math
import random
import sys

from rich.console import Console
from os.path import exists

console = Console()
"""Guess-My-Word is a game where the player has to guess a word.
Author: James Makela
Company: -
Copyright: 2023

"""
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

words_entered = []
keyboard = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
keymap = [keyboard.index(letter) for letter in "QWERTYUIOPASDFGHJKLZXCVBNM"]
stats_location = "./stats"


def play():
    """Code that controls the interactive game play"""
    # Initialise stats file if it does not exist
    init_stats()
    # select a word of the day:
    word_of_the_day = get_target_word().upper()
    # build a list of valid words (words that can be entered in the UI):
    valid_words = get_valid_words()
    # refresh the keyboard and used word list
    fresh_game()

    print_list = [" │ │ │ │ "] * MAX_ATTEMPTS
    for i in range(MAX_ATTEMPTS):
        guess = ask_for_guess(valid_words, print_list).upper()
        if guess.lower() == "exit":
            return
        score = score_guess(guess, word_of_the_day)
        print_list[i] = "│".join(colour_score(guess, score))
        if is_correct(score):
            output_buffer(print_list)
            console.print(f"Winner! Solved in {i + 1} guesses", justify="center")
            record_stats(True, i)
            console.print("Press enter to return to the menu", justify="center")
            input()
            return

    output_buffer(print_list)
    console.print("Try again next time", justify="center")
    console.print(f"The correct word was {word_of_the_day}", justify="center")
    record_stats(False)
    console.print("Press enter to return to the menu", justify="center")
    input()
    return True


def is_correct(score):
    """Checks if the score is entirely correct and returns True if it is
    """
    if score == (2, 2, 2, 2, 2):
        return True
    return False


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


def ask_for_guess(valid_words, buffer):
    guess = ''
    while guess is '' or guess.startswith('[red'):
        error = guess
        output_buffer(buffer)
        console.print("Type 'exit' to return to the main menu", justify="center")
        console.print(f" {error} ", justify="center")
        guess = guess_validator(valid_words)
        if guess == "exit":
            return guess
    words_entered.append(guess)
    return guess


def guess_validator(valid_words, override=None):
    """Requests a guess from the user directly from stdout/in
    Returns:
        str: the guess chosen by the user. Ensures guess is a valid word of correct length in lowercase
    """
    errors = ["[red on yellow]Invalid word[/]", "[red on yellow]Word already entered[/]"]
    if not override:
        guess_candidate = console.input(f"{' ' * (console.width // 2 - 8)}Guess: ").lower()
    else:
        guess_candidate = override
    if guess_candidate == "exit":
        return guess_candidate
    if guess_candidate not in valid_words:
        return errors[0]
    if guess_candidate in words_entered:
        return errors[1]
    if guess_candidate in valid_words and guess_candidate not in words_entered:
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


def colour_score(guess, score):
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


def output_buffer(list_to_print):
    console.clear()
    console.print("< WORDO >", justify="center")
    console.print("┌─┬─┬─┬─┬─┐", justify="center")
    for i, item in enumerate(list_to_print):
        console.print(f"│{item}│", justify="center")

        if i <= len(list_to_print) - 2:
            console.print("├─┼─┼─┼─┼─┤", justify="center")
    console.print("└─┴─┴─┴─┴─┘", justify="center")

    print_keyboard = []
    for number in keymap:
        print_keyboard.append(keyboard[number])

    console.print("".join(print_keyboard[:10]), justify="center")
    console.print(f" {''.join(print_keyboard[10:19])}", justify="center")
    console.print(f"  {''.join(print_keyboard[19:])}\n", justify="center")


def main_menu():
    while True:
        console.clear()
        console.print(
            "Welcome to Wordo, the word guessing game.\n"
            "Guess the 5 letter word in 6 tries or less.\n\n"
            "|  1 - Play Game    |\n"
            "|  2 - View Stats   |\n"
            "|  3 - View Help    |\n"
            "|  4 - Quit         |\n", justify="center")
        choice = input()
        if choice == "1":
            play()
        if choice == "2":
            view_stats()
        if choice == "3":
            game_help()
        if choice == "4":
            console.clear()
            sys.exit()


def init_stats():
    if not exists(stats_location):
        strings = [
            "Games played: 0\n",
            "Current streak: 0\n",
            "Max streak: 0\n",
            "Wins: 0\n"
            "1: 0\n",
            "2: 0\n",
            "3: 0\n",
            "4: 0\n",
            "5: 0\n",
            "6: 0\n"
        ]
        with open(stats_location, "w") as stats:
            stats.writelines(strings)


def record_stats(win, tries=0):
    strings = []
    with open(stats_location) as stats:
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

    with open(stats_location, "w") as stats:
        stats.writelines(strings)


def make_dict(stats):
    lines = {}
    for line in stats:
        line = line.split(":")
        lines[line[0]] = int(line[1])
    return lines


def view_stats():
    init_stats()
    console.clear()
    with open(stats_location) as stats:
        lines = make_dict(stats)

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


def fresh_game():
    global keyboard
    global words_entered
    keyboard = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    words_entered = []


def main():
    main_menu()


if __name__ == "__main__":
    main()
