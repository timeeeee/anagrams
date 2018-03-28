#include <stdexcept>
#include <iostream>

#include  "trie.h"

TrieNode::TrieNode() {
  // Initialize children to null
  for (int i = 0; i < 26; i++) {
    children[i] = NULL;
  }

  // If there was no root argument, make this the root
  root = this;

  // This is not an end of a word
  end = false;
}


TrieNode::TrieNode(TrieNode* pointerToRoot) {
  // Initialize children to null
  for (int i = 0; i < 26; i++) {
    children[i] = NULL;
  }

  root = pointerToRoot;

  // This is not the end of a word
  end = false;
}

TrieNode::~TrieNode() {
  for (int i = 0; i < 26; i++) {
    if (children[i] != NULL) {
      TrieNode* child = children[i];
      delete child;
    }
  }
}


// Add a word to the trie, starting at the first character
void TrieNode::add(std::string word) {
  add(word, 0);
}


// Add a word to the trie, starting at the given character
void TrieNode::add(std::string word, int start) {
  // Base case: nothing to add: word ends here
  if (start == word.length()) {
    end = true;
    return;
  }

  char first = word[start];
  if (!islower(tolower(first))) {
    std::string msg(1, first);
    msg += " is not a letter!";
    std::cout << msg << std::endl;
    throw std::invalid_argument(msg);
  }
  int index = tolower(first) - 'a';

  // otherwise, add a child for the first letter if necessary...
  if (children[index] == NULL) {
    children[index] = new TrieNode(root);
  }

  // ... and add the rest of the word to that node
  children[index]->add(word, start + 1);
}


// Is the given word in the trie?
bool TrieNode::isWord(std::string word) {
  return isWord(word, 0);
}


// Is the given word, starting from index 'start', in the trie?
bool TrieNode::isWord(std::string word, int start) {
  // Base case: empty string. true if this trie node is the end of a word.
  if (start == word.length()) {
    return end;
  }

  char first = word[start];
  if (!islower(tolower(first))) {
    throw std::invalid_argument(first + " is not a letter!");
  }
  int index = tolower(first) - 'a';

  // Otherwise, is the rest of the word in the child trie?
  TrieNode* child = children[index];
  if (child == NULL) return false;
  return child->isWord(word, start + 1);
}


void TrieNode::print() {
  print(0);
}


void TrieNode::print(int depth) {
  for (int indent = 0; indent < depth; indent++) std::cout << "  ";
  if (end) std::cout << "word ends here\n";

  for (int i = 0; i < 26; i++) {
    TrieNode* child = children[i];
    if (child != NULL) {
      char letter = i + 'a';
      for (int indent = 0; indent < depth; indent++) std::cout << "  ";
      std::cout << letter << ":\n";
      child->print(depth + 1);
    }
  }
}
