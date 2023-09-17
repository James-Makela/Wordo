#!/usr/bin/env python3
import random
from rich.console import Console
console = Console()
"""Guess-My-Word is a game where the player has to guess a word.
<your description> 
Author: <name>
Company: <company>
Copyright: <year>

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

ALL_WORDS = './word-bank/all_words.txt'
TARGET_WORDS = './word-bank/target_words.txt'

words_entered = []

keyboard = [chr(i) for i in range(ord('A'), ord('Z')+1)]
keymap = [keyboard.index(letter) for letter in 'QWERTYUIOPASDFGHJKLZXCVBNM']


def play():
    """Code that controls the interactive game play"""
    # select a word of the day:
    word_of_the_day = get_target_word().upper()
    # build a list of valid words (words that can be entered in the UI):
    valid_words = get_valid_words()
    # do the following in an iteration construct
    print_list = [" │ │ │ │ "] * MAX_ATTEMPTS
    main_menu()
    for i in range(MAX_ATTEMPTS):
        output_buffer(print_list)
        guess = ask_for_guess(valid_words).upper()
        score = score_guess(guess, word_of_the_day)
        # Put some of your own personality into this!
        print("Result of your guess:")
        # print(f"{format_score(guess, score)}\n")
        print_list[i] = "│".join(colour_score(guess, score))
        if is_correct(score):
            output_buffer(print_list)
            console.print(f"Winner! Solved in {i + 1} guesses", justify="center")
            return
        # end iteration
    output_buffer(print_list)
    console.print("Try again next time", justify="center")
    console.print(f"The correct word was {word_of_the_day}", justify="center")
    return True


def is_correct(score):
    """Checks if the score is entirely correct and returns True if it is
    Examples:
    >>> is_correct((1,1,1,1,1))
    False
    >>> is_correct((2,2,2,2,1))
    False
    >>> is_correct((0,0,0,0,0))
    False
    >>> is_correct((2,2,2,2,2))
    True"""
    if score == (2, 2, 2, 2, 2):
        return True
    return False


def get_valid_words(file_path=ALL_WORDS):
    """returns a list containing all valid words.
    Note to test that the file is read correctly, use:
    >>> get_valid_words()[0]
    'aahed'
    >>> get_valid_words()[-1]
    'zymic'
    >>> get_valid_words()[10:15]
    ['abamp', 'aband', 'abase', 'abash', 'abask']

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

    How do you test that a random word chooser is choosing the correct words??
    Discuss in class!
    >>> get_target_word(seed=0)
    'aback'
    >>> get_target_word(seed=-1)
    'zonal'

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


def ask_for_guess(valid_words):
    """Requests a guess from the user directly from stdout/in
    Returns:
        str: the guess chosen by the user. Ensures guess is a valid word of correct length in lowercase
    """
    guess = None
    while guess is None:
        guess_candidate = console.input(f'{" " * (console.width // 2 - 8)}Guess: ').lower()
        if guess_candidate in valid_words and guess_candidate not in words_entered:
            guess = guess_candidate
            words_entered.append(guess_candidate)
    return guess_candidate


def score_guess(guess, target):
    """given two strings of equal length, returns a tuple of ints representing the score of the guess
    against the target word (MISS, MISPLACED, or EXACT)
    Here are some example (will run as doctest):

    >>> score_guess('hello', 'hello')
    (2, 2, 2, 2, 2)
    >>> score_guess('drain', 'float')
    (0, 0, 1, 0, 0)
    >>> score_guess('hello', 'spams')
    (0, 0, 0, 0, 0)

    Try and pass the first few tests in the doctest before passing these tests.
    >>> score_guess('gauge', 'range')
    (0, 2, 0, 2, 2)
    >>> score_guess('melee', 'erect')
    (0, 1, 0, 1, 0)
    >>> score_guess('array', 'spray')
    (0, 0, 2, 2, 2)
    >>> score_guess('train', 'tenor')
    (2, 1, 0, 0, 1)
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


def help():
    """Provides help for the game"""
    console.clear()
    console.print('HALP!')
    input()


def format_score(guess, score):
    """Formats a guess with a given score as output to the terminal.
    The following is an example output (you can change it to meet your own creative ideas, 
    but be sure to update these examples)
    >>> print(format_score('hello', (0,0,0,0,0)))
    H E L L O
    _ _ _ _ _
    >>> print(format_score('hello', (0,0,0,1,1)))
    H E L L O
    _ _ _ ? ?
    >>> print(format_score('hello', (1,0,0,2,1)))
    H E L L O
    ? _ _ + ?
    >>> print(format_score('hello', (2,2,2,2,2)))
    H E L L O
    + + + + +"""

    print_item = []
    for i in range(5):
        if score[i] == MISS:
            print_item.append('_ ')
        elif score[i] == MISPLACED:
            print_item.append('? ')
        elif score[i] == EXACT:
            print_item.append('+ ')
    return_string = ""
    for letter in guess:
        return_string += f'{letter.upper()} '
    return_string = return_string.rstrip()
    return_string += '\n'
    for item in print_item:
        return_string += item
    return return_string.rstrip()


def colour_score(guess, score):
    print_item = []
    for i, letter in enumerate(guess):
        if score[i] == 0:
            style = 'white on #666666'
            # TODO: Simplify this
            if 'green' not in keyboard[ord(letter) - ord('A')] and 'yellow' not in keyboard[ord(letter) - ord('A')]:
                keyboard[ord(letter) - ord('A')] = " "
        elif score[i] == 1:
            style = "bold black on yellow"
            if 'green' not in keyboard[ord(letter) - ord('A')]:
                keyboard[ord(letter) - ord('A')] = f"[{style}]{letter}[/]"
        elif score[i] == 2:
            style = "bold black on green"
            keyboard[ord(letter) - ord('A')] = f"[{style}]{letter}[/]"

        print_item.append(f"[{style}]{guess[i]}[/]")
    return print_item


# Normal mode
def print_guess(print_string):
    # TODO: Does this need to be a function?
    console.print(f'{"".join(print_string)}')


def output_buffer(list):
    console.clear()
    console.print("< WORDO >", justify="center")
    console.print("┌─┬─┬─┬─┬─┐", justify="center")
    for i, item in enumerate(list):
        console.print(f"│{item}│", justify="center")

        if i <= len(list) - 2:
            console.print("├─┼─┼─┼─┼─┤", justify="center")
    console.print("└─┴─┴─┴─┴─┘", justify="center")

    print_keyboard = []
    for number in keymap:
        print_keyboard.append(keyboard[number])

    console.print("".join(print_keyboard[:10]), justify="center")
    console.print(f' {"".join(print_keyboard[10:19])}', justify="center")
    console.print(f'  {"".join(print_keyboard[19:])}', justify="center")


def main_menu():
    console.clear()
    console.print(
                  "Welcome to Wordo, the word guessing game.\n"
                  "Guess the 5 letter word in 6 tries or less.\n\n"
                  "Press enter to play, or type help and press\n"
                  "enter to view help", justify="center")
    if input().lower() == 'help':
        help()


def main(test=False):
    if test:
        import doctest
        return doctest.testmod()
    play()
    return "Goodbye"


if __name__ == '__main__':
    # print(main(test=True))
    main()
