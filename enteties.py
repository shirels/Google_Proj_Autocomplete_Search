from dataclasses import dataclass



@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int

    # methods that you need to define by yourself

    #TODO: insert function that whoul limit items to 5 items
    def __init__(self, sentence: str, source: str, offs: int):
        self.completed_sentence = sentence
        self.offset = offs
        self.source_text = source
        self.score = 0

    def add_score(self, score_: int):
        self.score += score_ * 2

    def print_suggest(self):
        print(f"{self.completed_sentence[:-1]}  ({self.source_text} {self.offset} {self.score})")


@dataclass
class TrieNode:
    def __init__(self):
        self.children = dict()
        self.end_sen = False
        self.best_5_sen = list()
        self.depth = 0

    def add_sentence(self, suggest: AutoCompleteData):
        if len(self.best_5_sen) == 5:
            self.best_5_sen.append(suggest)
            self.best_5_sen = sorted(self.best_5_sen, key=lambda sentence: sentence.completed_sentence.strip().lower())
            self.best_5_sen = self.best_5_sen[:-1]
        else:
            self.best_5_sen.append(suggest)
        self.best_5_sen = sorted(self.best_5_sen, key=lambda sentence: sentence.completed_sentence.lower())

    def set_depth(self, d: int):
        self.depth = d