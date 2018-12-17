//
// Created by laomd on 2018/12/17.
//

#include "trie.h"

TrieNode* TrieNode::insert(string::const_iterator first, string::const_iterator last) {
    if (first == last) {
        return nullptr;
    }
    else {
        TrieNode *child = _children[*first];
        if (child == nullptr)
            child = _children[*first] = new TrieNode;
        if ((_children[*first] = child->insert(first + 1, last)) == nullptr)
            delete child;
        return this;
    }
}

string TrieNode::keys() const {
    string res;
    for (auto& item: _children)
        res += item.first;
    return res;
}

vector<TrieNode *> TrieNode::children() const {
    vector<TrieNode *> res;
    for (auto& item: _children)
        res.push_back(item.second);
    return res;
}

void bfs(TrieNode* root) {
    queue<TrieNode*> nq;
    nq.push(root);
    while (!nq.empty()) {
        TrieNode* node = nq.front();
        nq.pop();
        if (node) {
            cout << node->keys() << endl;
            for (auto child: node->children()) {
                nq.push(child);
            }
        }
    }
}
