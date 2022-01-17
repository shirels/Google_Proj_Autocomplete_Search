from enteties import AutoCompleteData, TrieNode
import re


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


def calc_score(user_query: str, data: str):
    mistake_flag = False
    add_del_flag = False
    save_index = 0
    index = 0
    sub = 0
    if abs(len(user_query) - len(data)) > 1:
        return False, sub
    # adding or subtracting a word
    elif abs(len(user_query) - len(data)) == 1:
        add_del_flag = True
        # user_query the long word, data the short word
        if len(user_query) > len(data):
            word1 = user_query
            word2 = data
        else:
            word1 = data
            word2 = user_query
        for letter in word1:
            if len(word2) == index and mistake_flag:
                return False, sub
            elif len(word2) == index:
                save_index = index
                break
            elif letter != word2[index]:
                if mistake_flag:
                    return False, sub
                mistake_flag = True
                save_index = index
            else:
                index += 1
    else:
        for letter in user_query:
            if letter != data[index]:
                if mistake_flag:
                    return False, sub
                mistake_flag = True
                save_index = index
            index += 1
    if save_index > 3:
        sub = 1
    else:
        sub = 5 - save_index
    if add_del_flag:
        sub *= 2
    return True, sub
