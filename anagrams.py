from string import ascii_lowercase as lowercase
from collections import Counter
from sys import argv

from nose.tools import *


class Trie(object):
    """
    A node in a trie.

    For all valid next letters, self.children[char] will point to another Trie
    object representing the remaining possible word endings. If it's valid for
    a word to end here, self.children[END] will point to the root of the Trie.
    """
    def __init__(self, wordlist=[], root=None):
        """
        Initialize a trie, with the words in wordlist
        """
        self.children = dict()

        # Is it valid for a word to end here?
        self.end = False

        # Root of the trie
        self.root = self if root is None else root
        
        for word in wordlist:
            self.add(word)

    def add(self, word):
        """Add a word to the trie"""
        # Base case: empty string. We are at a word ending.
        if word == "":
            self.end = True
        else:
            first_char = word[0].lower()
            if first_char not in self.children:
                self.children[first_char] = Trie(root=self.root)

            self.children[first_char].add(word[1:])
        
    def __contains__(self, word):
        # Base case: empty string. true if this is a valid end of a word
        if word == "":
            return self.end

        # Otherwise, make sure there is a child corresponding to the first char
        first_char = word[0].lower()
        if first_char not in self.children:
            return False

        # Is the rest of the word in the child trie?
        return (word[1:] in self.children[first_char])

    def to_json(self):
        json = dict()

        if self.end:
            json["end"] = True
            
        for char in self.children:
            json[char] = self.children[char].to_json()

        return json


with open("english_words.txt") as f:
    ENGLISH_TRIE = Trie(line.strip() for line in f)

with open("enable1.txt") as f:
    OVERKILL_TRIE = Trie(line.strip() for line in f)


def test_wordlist_trie():
    with open("english_words.txt") as f:
        for line in f:
            word = line.strip().lower()
            assert_in(word, ENGLISH_TRIE)


def test_trie_wordlist_argument():
    with open("english_words.txt") as f:
        wordlist = [line.strip().lower() for line in f]

    trie = Trie(wordlist)

    for word in wordlist:
        assert_in(word, trie)


def test_no_fake_words():
    not_words = [
        "", "flarpy", "queem", "b"
    ]

    for not_word in not_words:
        assert_not_in(not_word, ENGLISH_TRIE)


def find_anagrams(letters):
    pass


def _find_anagrams(available, trie, this_word="", last_word=None, depth=0):
    """
    Find all anagrams that can be made with the given letters, where available
    is a dictionary of how many of each letter are left. Trie is the node of a
    trie to build words from. Yield each solution as a list of strings.
    """
    # print("  " * depth + this_word + "... ?")

    # Base case:
    # No letters left! this is an anagram IF a word can end here on the trie
    if all(x == 0 for x in available.values()):
        if trie.end:
            # yield one empty solution
            yield [""]
        else:
            # no solutions
            raise StopIteration

    # Otherwise try each available letter
    for char in lowercase:
        # LOTS of conditions. Only use this letter if:
        # ... we have it left to use
        is_available = char in available and available[char] > 0
        # ... it's a valid next letter in the current word
        is_valid = char in trie.children
        # ... and, it maintains alphabetical order of words in the result
        is_alphabetical = last_word is None or char >= last_word[0]

        if is_available and is_valid and is_alphabetical:
            # Find all anagrams of the remaining characters!
            # counts will be passed by reference so modify this first
            available[char] -= 1
            next_trie = trie.children[char]  # advance one letter in the trie
            next_last_word = None  # next line might set this
            if last_word is not None and len(last_word) > 1:
                next_last_word = last_word[1:]
            answers = _find_anagrams(
                available, next_trie, this_word + char, next_last_word, depth + 1)
            for first, *rest in answers:
                yield [char + first] + rest

            # change the counts back before moving on to the next letter!
            available[char] += 1

    # Also if this is a valid word ending, we can start a new word:
    if trie.end:
        for solution in _find_anagrams(available, trie.root, last_word=this_word, depth=depth + 1):
            # (The calling functions will add letters to the empty string)
            yield [""] + solution


def test_find_anagrams_one_letter():
    trie = Trie(["a"])
    a = list(_find_anagrams({"a": 1}, trie))
    assert_list_equal(a, [["a"]])


def test_cat_anagrams():
    cat_anagrams = list(_find_anagrams(Counter("cat"), ENGLISH_TRIE))
    assert_list_equal(sorted(cat_anagrams), [["act"], ["cat"]])


if __name__ == "__main__":
    if len(argv) == 1:
        print("use: python3 anagrams.py <phrase to make anagrams of>")
        exit(0)
    
    available = Counter()
    for word in argv[1:]:
        available.update(char for char in word.lower() if char in lowercase)

    for anagram in _find_anagrams(available, ENGLISH_TRIE):
        print(anagram)
