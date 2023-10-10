from app.wordo import get_target_word
from app.wordo import score_guess
from app.wordo import is_correct
from app.wordo import guess_validator
from app.wordo import get_valid_words
from app.wordo import colour_score


def test_is_correct():
    assert not is_correct((1, 1, 1, 1, 1))
    assert not is_correct((2, 2, 2, 2, 1))
    assert not is_correct((0, 0, 0, 0, 0))
    assert is_correct((2, 2, 2, 2, 2))


def test_get_valid_words():
    assert get_valid_words()[0] == 'aahed'
    assert get_valid_words()[-1] == 'zymic'
    assert get_valid_words()[10:15] == ['abamp', 'aband', 'abase', 'abash', 'abask']


def test_get_target_word():
    assert get_target_word(seed=0) == 'aback'
    assert get_target_word(seed=-1) == 'zonal'
    assert get_target_word(seed=600) == 'drone'


def test_guess_validator():
    valid_words = get_valid_words()

    assert guess_validator(valid_words, override="round") == "round"
    assert guess_validator(valid_words, override="steam") == "steam"
    assert guess_validator(valid_words, override="panda") == "panda"
    assert guess_validator(valid_words, override="zobra") == "[red on yellow]Invalid word[/]"


def test_score_guess():
    assert score_guess('hello', 'hello') == (2, 2, 2, 2, 2)
    assert score_guess('drain', 'float') == (0, 0, 1, 0, 0)
    assert score_guess('hello', 'spams') == (0, 0, 0, 0, 0)
    assert score_guess('gauge', 'range') == (0, 2, 0, 2, 2)
    assert score_guess('melee', 'erect') == (0, 1, 0, 1, 0)
    assert score_guess('array', 'spray') == (0, 0, 2, 2, 2)
    assert score_guess('train', 'tenor') == (2, 1, 0, 0, 1)


def test_colour_score():
    grey = "#666666"
    yellow = "#d1b036"
    green = "#6aaa64"
    assert colour_score("H", (0,)) == [f"[white on {grey}]H[/]"]
    assert colour_score("E", (1,)) == [f"[bold black on {yellow}]E[/]"]
    assert colour_score("L", (2,)) == [f"[bold black on {green}]L[/]"]


def main():
    test_get_target_word()
    test_score_guess()
    test_get_valid_words()
    test_is_correct()
    test_guess_validator()
    test_colour_score()


if __name__ == "__main__":
    main()
