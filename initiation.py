from enteties import AutoCompleteData, TrieNode
# from sortedcontainers import SortedList
from dataclasses import dataclass
import re
from complition import get_best_k_completions




def insert_word(root: TrieNode, s_words: list, line: str, source: str, off: int):
    count = 0
    depth = 0
    for s_word in s_words:
        count += len(s_word)
        depth += 1
        if s_word not in root.children.keys():
            root.children[s_word] = TrieNode()
            root.children[s_word].set_depth(depth)
        source = source[:source.rfind('.')]
        auto_comp = AutoCompleteData(sentence=line, source=source, offs=off)
        auto_comp.add_score(count)
        root.children[s_word].add_sentence(auto_comp)
        root = root.children[s_word]


def initiation(path: str) -> dict:
    # 1. read from path
    # TODO: read from dir tree
    my_file = open(path, 'r')
    lines = my_file.readlines()  # list of str

    # 2. build prefix data tree
    prefix_tree_root = TrieNode()
    line_num = 0
    for line in lines:
        line_num += 1
        tmp_line = re.sub('[,.?!*(*+)=(=+)]', '', line).lower()
        words = tmp_line.split()
        for word in words:
            indx = words.index(word)
            insert_word(prefix_tree_root, words[indx: min(len(words), indx+10)], line, path, line_num)
    return prefix_tree_root


