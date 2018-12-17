//
// Created by laomd on 2018/12/17.
//
#include <iostream>
#include <queue>
#include "../trie.h"
using namespace std;

int main() {
    TrieNode root;
    string a("apple"), b("bob"), c("apabic");
    insert(&root, a.begin(), a.end());
    insert(&root, b.begin(), b.end());
    insert(&root, c.begin(), c.end());
    bfs(&root);
    return 0;
}