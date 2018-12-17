//
// Created by laomd on 2018/12/17.
//

#include "trie.h"

bool TrieNode::insert(string::const_iterator first, string::const_iterator last) {
    if (first == last) {
        return false;
    }
    else {
        bool is_word;
        TrieNode *child;
        tie(is_word, child) = _children[*first];
        if (child == nullptr)
            child = new TrieNode;
        bool flag = child->insert(first + 1, last);
        is_word = is_word || !flag;
        if (!flag) {
            delete child;
            child = nullptr;
        }
        _children[*first] = make_pair(is_word, child);
        return true;
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
        res.push_back(item.second.second);
    return res;
}

pair<bool, TrieNode*> TrieNode::get_child(char c) {
    if (_children.find(c) != _children.end())
        return _children[c];
    else
        return make_pair(false, nullptr);
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
