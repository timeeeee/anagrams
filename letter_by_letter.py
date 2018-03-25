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


def test_wordlist_trie():
    trie = Trie()
    with open("english_words.txt") as f:
        for line in f:
            word = line.strip().lower()
            trie.add(word)

            assert_in(word, trie)


def test_trie_wordlist_argument():
    with open("english_words.txt") as f:
        wordlist = [line.strip().lower() for line in f]

    trie = Trie(wordlist)

    for word in wordlist:
        assert_in(word, trie)


def test_no_fake_words():
    with open("english_words.txt") as f:
        trie = Trie(line.strip() for line in f)

    not_words = [
        "", "flarpy", "queem", "b"
    ]

    for not_word in not_words:
        assert_not_in(not_word, trie)


def find_anagrams(letters):
    pass


def _find_anagrams():
    """
    """
    pass



if __name__ == "__main__":
    with open("english_words.txt") as f:
        trie = Trie(line.strip() for line in f)

    import json

    with open("trie.json", "w") as f:
        json.dump(trie.to_json(), f)
