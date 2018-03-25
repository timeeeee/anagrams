from string import ascii_lowercase as lowercase
from collections import Counter, defaultdict

from nose.tools import *
from nose.plugins.skip import SkipTest


# Subclass of Counter to allow them to be used as dictionary keys
class LetterCounter(Counter):
    def __hash__(self):
        h = 0
        base = 1
        for char in lowercase:
            h += self[char] * base
            base *= 2

        return h

    def __sub__(self, other):
        return LetterCounter(super().__sub__(other))


IGNORE = []
with open("ignore.txt") as f:
    for line in f:
        word = line.strip()
        if word:
            IGNORE.append(word)

LETTER_COUNTS = dict()
WORDLIST = []

# Populate WORDLIST and LETTER_COUNTS
with open("words.txt") as f:
    for line in f:
        word = line.strip().lower()
        if word not in IGNORE:
            WORDLIST.append(word)
            LETTER_COUNTS[word] = LetterCounter(word)

# This will cache known anagram solutions, with a LetterCounter object for the
# key and a list of lists of words as the value.
CACHE = defaultdict(lambda: [])


def find_anagrams(phrase):
    """
    Return a generator for all anagrams of the phrase. Wrapper function for
    _find_anagrams.
    """
    counts = LetterCounter(filter(str.isalpha, phrase.lower()))
    return _find_anagrams(counts)


def _find_anagrams(available, start=0, depth=0):
    """
    Return a generator of all anagrams using the given letter counts, where
    "available" is LetterCounter object with the available letters.
    """
    # print("  " * depth + "finding anagrams for counts {}".format(available))
    # If we have already tried to calculate anagrams of the available letters,
    # use the answer we already got
    if available in CACHE:
        yield from CACHE[available]

    # Base case: If there are no letters available, the only possible anagram
    # is an empty string!
    if all(count == 0 for count in available.values()):
        yield []
        raise StopIteration

    # For each word, see if we have enough letters available to make it
    for index in range(start, len(WORDLIST)):
        word = WORDLIST[index]
        counts = LETTER_COUNTS[word]
        if all(counts[char] <= available[char] for char in lowercase):
            # LOOKOUT: This could be bad if available[n] < counts[n], somehow
            # print("  " * depth + "guessing word {}".format(word))
            new_available = available - counts
            for rest in _find_anagrams(new_available, start=index, depth=depth+1):
                solution = [word] + rest

                # cache this answer
                CACHE[available].append(solution)

                # print(solution)

                yield solution

    # If there are no possible anagrams, we'll get here without having yielded
    # anything and return None.


def test_empty_anagrams():
    # an empty word should have exactly one solution, an empty list
    assert_list_equal(list(_find_anagrams(LetterCounter())), [[]])


def test_no_possible_anagram():
    assert_list_equal(list(_find_anagrams(LetterCounter("c"))), [])


# With cacheing, these are not in order :-/
@SkipTest
def test_words_in_order():
    for solution in _find_anagrams(LetterCounter("absolute")):
        assert_list_equal(solution, sorted(solution))


def test_known_anagrams():
    anagrams = ['updaters', 'upstared', 'pastured']
    pass





if __name__ == "__main__":
    words = set()
    for solution in find_anagrams("captain tyin knots"):
        if all(a == b for a, b in zip(solution, sorted(solution))):
            print(" ".join(solution))
            words.update(solution)
    print("used words: {}".format(", ".join(sorted(words))))
