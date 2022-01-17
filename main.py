import re

from complition import calc_score
from enteties import TrieNode
from initiation import initiation


def get_best_k_completions_rec(words: list[str], root: TrieNode, lst_result: list,
                               f_m: bool):  # ->  list[AutoCompleteData]:
    if not words:
        lst_result += root.best_5_sen
        return lst_result
    if not root.children:
        return lst_result
    # step
    for word in words:
        word_not_found = True
        # Search the word through all the children of the present `node`
        for c_key, c_value in root.children.items():
            if c_key == word:
                # We found the char existing in the child.
                word_not_found = False
                get_best_k_completions_rec(words[words.index(word) + 1:], c_value, lst_result, f_m)

        # when we did not find the word, check mistake.
        if word_not_found:
            for c_key, c_value in root.children.items():
                mistake_flag, sub_score = calc_score(word, c_key)
                if mistake_flag and f_m:
                    get_best_k_completions_rec(words[words.index(word) + 1:], c_value, lst_result, False)
    return lst_result


def get_best_k_completions(query: str, root: TrieNode):
    query_tmp = re.sub(r'[.?!]', '', query).lower()
    words = query_tmp.split()
    # if there was already a mistake
    first_mistake = True
    return get_best_k_completions_rec(words, root, [], first_mistake)


if __name__ == '__main__':
    print("Loading the file and preparing the system...")
    d = initiation('stam.txt')
    text = input("The system is ready. Enter your text:\n")
    while text.find("#") == -1:
        li = get_best_k_completions(text, d)
        index = 1
        print("Here are 5 suggestion: ")
        if li:
            for i in li:
                print(str(index) + ". ", end=" ")
                i.print_suggest()
                index += 1
        print(text, end=" ")
        text += " "
        text += input()
