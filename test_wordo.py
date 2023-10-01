from wordo import get_target_word
from wordo import score_guess
from wordo import is_correct
from wordo import guess_validator
from wordo import get_valid_words


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


def test_guess_validator(monkeypatch):
    testlist = ['round', 'steam', 'zobra', 'panda']
    valid_words = get_valid_words()

    for word in testlist:

        if word not in valid_words:
            assert guess_validator(valid_words, word) == (None, 1)
        else:
            assert guess_validator(valid_words, word) == (word, 0)


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
    test_score_guess()
    test_get_valid_words()
    test_is_correct()
    test_guess_validator()


if __name__ == "__main__":
    main()
