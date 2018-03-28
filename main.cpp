#include <iostream>
#include <fstream>
#include <string>
#include <cassert>

#include "trie.h"

void printIsInTrie(TrieNode& trie, std::string word);
void findAnagrams(std::string phrase, TrieNode& trie);
void findAnagrams(int available[], TrieNode& trie, std::string thisWord, std::string lastWord);





int main() {
  TrieNode trie;

  std::ifstream wordlist("english_words.txt");
  std::string word;
  while (wordlist >> word) {
    trie.add(word);
  }

  findAnagrams("you chunnin' bro?", trie);


  return 0;
}


void printIsInTrie(TrieNode& trie, std::string word) {
  std::cout << "\"" << word << "\" is ";
  if (!trie.isWord(word)) std::cout << "not ";
  std::cout << "in the trie.\n";
}



// Get a count of each letter in phrase, and call the recursive anagram function
void findAnagrams(std::string phrase, TrieNode& trie) {
  int counts[26];
  for (int i = 0; i < 26; i++) {
    counts[i] = 0;
  }

  for (int i = 0; i < phrase.length(); i++) {
    if (isalpha(phrase[i])) {
      counts[tolower(phrase[i]) - 'a']++;
    }
  }

  findAnagrams(counts, trie, "", "");
}

void findAnagrams(int available[], TrieNode& trie, std::string thisWord, std::string lastWord) {
  std::cout << "finding anagrams!\n";
}
