import string
import time


class Node:

    def __init__(self, value):
        self.children = []
        self.value = value
        self.endOfWords = [0] * 11
        self.docIds = []

    def add_docId(self, doc_id):
        self.docIds.append(doc_id)

    def inc_end_of_word(self, doc_id):
        self.endOfWords[doc_id] += 1


class Tree:
    hashmap = {}  # a map from valid strings found in dfs -> list of docIds related to EndOfWord char

    def __init__(self):
        self.root = self.create_root()

    def create_root(self):
        return Node(None)

    def insert(self, to_insert, doc_id):
        current_element_tree = self.root
        length_word = len(to_insert)
        for i in range(length_word):
            processed_char = lower_case_char(to_insert[i])
            next_element_tree = None
            for child in current_element_tree.children:
                if child.value == processed_char:
                    next_element_tree = child
                    break
            if next_element_tree is None:
                next_element_tree = Node(to_insert[i])
                current_element_tree.children.append(next_element_tree)
            next_element_tree.add_docId(doc_id)
            if i == length_word - 1:
                next_element_tree.inc_end_of_word(doc_id)
            current_element_tree = next_element_tree

    def find(self, to_find):
        iterator = self.root
        i = 0
        while len(iterator.children) != 0:
            found = False
            for child in iterator.children:
                if child.value == to_find[i]:
                    iterator = child
                    i += 1
                    found = True
                    break
            if not found:
                return None
            if i == len(to_find):
                return iterator


def lower_case_char(char):
    if ord(char) < 97:
        char = chr(ord(char) + 32)  # lowercase the uppercase letters
    return char


def dfs(node, st):
    li = []
    st = st + node.value
    added = False
    for i in range(1, 11):  # i = different doc ids
        end_of_word_i = node.endOfWords[i]  # number of occurrence of current string in doc[i]
        string_seen_before = st in Tree.hashmap
        if string_seen_before:
            Tree.hashmap[st][i] = Tree.hashmap[st][i] + end_of_word_i
        else:
            Tree.hashmap[st] = [0] * 11
            Tree.hashmap[st][i] = end_of_word_i
        if end_of_word_i > 0 and not added:
            li.append(st)
            added = True
    for child in node.children:
        li.extend(dfs(child, st))
    return li


def answer_a_query(tree_n, tree_r, pattern, result_file):
    count_in_doc = [(0, i) for i in range(11)]
    # extract letters into two parts -> p1:(before '\S*') p2:(after '\S*')
    parts = pattern.split('\\S*')
    # lower case letters of each part
    parts[0] = ''.join(x for x in parts[0] if x.isalpha()).lower()
    parts[1] = ''.join(x for x in parts[1] if x.isalpha()).lower()
    # reverse second part
    parts[1] = parts[1][::-1]
    # last letters of each substring
    last_letter_normal = None
    last_letter_reversed = None
    if len(parts[0]) != 0:
        last_letter_normal = tree_n.find(parts[0])
    else:
        last_letter_normal = Node('-1')
    if len(parts[1]) != 0:
        last_letter_reversed = tree_r.find(parts[1])
    else:
        last_letter_reversed = Node('-1')
    # case: pattern didn't match:
    if last_letter_reversed is None or last_letter_normal is None:
        print(-1)
    else:
        list_normal = []
        list_reversed = []

        if last_letter_normal.value != '-1' and last_letter_reversed.value != '-1':
            list_normal = dfs(last_letter_normal, parts[0][0:len(parts[0]) - 1:])
            list_reversed = dfs(last_letter_reversed, parts[1][0:len(parts[1]) - 1:])
            list_final = []

            for st in list_normal:
                if (st[::-1] in list_reversed) and (len(st) >= len(parts[0]) + len(parts[1])):
                    for i in range(1, 11):
                        count_in_doc[i] = (count_in_doc[i][0] + Tree.hashmap[st][i], i)

        elif last_letter_normal.value != '-1' and last_letter_reversed.value == '-1':
            list_normal = dfs(last_letter_normal, parts[0][0:len(parts[0]) - 1:])

            for st in list_normal:
                for i in range(1, 11):
                    count_in_doc[i] = (count_in_doc[i][0] + Tree.hashmap[st][i], i)


        elif last_letter_normal.value == '-1' and last_letter_reversed.value != '-1':
            list_reversed = dfs(last_letter_reversed, parts[1][0:len(parts[1]) - 1:])

            for st in list_reversed:
                for i in range(1, 11):
                    count_in_doc[i] = (count_in_doc[i][0] + Tree.hashmap[st][i], i)

        else:
            list_ = []
            for child in tree_n.root.children:
                list_.extend(dfs(child, ''))
            for st in list_:
                for i in range(1, 11):
                    count_in_doc[i] = (count_in_doc[i][0] + Tree.hashmap[st][i], i)

        copy_count_in_doc = count_in_doc.copy()
        list_to_print = []
        for i in range(1, 11):
            max_index = 0
            for j in range(1, 11):
                if count_in_doc[j][0] > count_in_doc[max_index][0]:
                    max_index = j
            list_to_print.append(max_index)
            count_in_doc[max_index] = (0, max_index)

        written = False
        str_to_print = ''
        for i in list_to_print:
            if copy_count_in_doc[i][0] != 0:
                written = True
                str_to_print += str(i)
                str_to_print += ' '
            else:
                break
        if not written:
            result_file.write('-1\n')
        else:
            result_file.write(str_to_print[0:len(str_to_print) - 1:1])
            result_file.write('\n')


def main():
    # preprocess and organization of data
    # one tree without reversing the words:
    tree_normal = Tree()
    tree_reversed = Tree()
    words = []
    for i in range(10):
        doc = open(f"doc{i + 1:02}.txt", mode='r', encoding="utf8")
        for word in doc.readline().strip().split(' '):
            to_insert = ''.join(x for x in word if x.isalpha()).lower()
            tree_normal.insert(to_insert, i + 1)
            tree_reversed.insert(to_insert[::-1], i + 1)
        doc.close()

    # inputting queries
    input_file = open("input.txt", mode='r')
    queries_count = int(input_file.readline())
    queries: list[string] = input_file.read().splitlines()

    result_file = open('result.txt', mode='w')
    start_time = time.time()
    # answering queries
    for query in queries:
        answer_a_query(tree_normal, tree_reversed, query, result_file)
    end_time = time.time()
    duration = (end_time - start_time) / 1_000_000

    time_file = open("time.txt", mode='w')
    time_file.write(str(duration))
    time_file.close()
    print("time of answering input:", duration)


if __name__ == '__main__':
    main()
