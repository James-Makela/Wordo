import pytest
from wordo import get_target_word
from wordo import score_guess


def test_get_target_word():
    assert get_target_word(seed=0) == 'aback'
    assert get_target_word(seed=-1) == 'zonal'
    assert get_target_word(seed=600) == 'drone'


def test_score_guess():
    assert score_guess('hello', 'hello') == (2, 2, 2, 2, 2)
    assert score_guess('drain', 'float') == (0, 0, 1, 0, 0)
    assert score_guess('hello', 'spams') == (0, 0, 0, 0, 0)
    assert score_guess('gauge', 'range') == (0, 2, 0, 2, 2)
    assert score_guess('melee', 'erect') == (0, 1, 0, 1, 0)
    assert score_guess('array', 'spray') == (0, 0, 2, 2, 2)
    assert score_guess('train', 'tenor') == (2, 1, 0, 0, 1)


def main():
    test_get_target_word()


if __name__ == "__main__":
    main()