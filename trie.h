#ifndef __TRIE_H_
#define __TRIE_H_

#include <string>

#endif

/* 
 * A single node in a Trie. Can be root, or not.
 */
class TrieNode {
 public:
  TrieNode* children[26];
  TrieNode* root;
  bool end;

  // Initialize an empty trie
  TrieNode();
  TrieNode(TrieNode* pointerToRoot);
  ~TrieNode();
  void add(std::string word);
  void add(std::string word, int start);
  bool isWord(std::string word);
  bool isWord(std::string word, int start);
  void print();
  void print(int depth);
};
  
  
