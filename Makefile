ALL: trie.o main.o
	g++ -g trie.o main.o -o anagrams

trie.o: trie.h trie.cpp
	g++ -c -g trie.cpp

main.o: main.cpp
	g++ -c -g main.cpp

.PHONY: clean

clean:
	rm -f *~ *.o anagrams
