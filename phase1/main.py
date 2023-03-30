import string
import re


class Node:

    def __init__(self, value: string):
        self.children = []
        self.value = value
        self.numberOfEndOfWord = 0

    def inc_end_of_word(self):
        self.numberOfEndOfWord += 1


class Tree:

    def __init__(self):
        self.root = self.create_root()

    def create_root(self):
        return Node(None)

    def insert(self, to_insert: string):
        current_element_tree = self.root
        length_word = len(to_insert)
        for i in range(length_word):
            processed_char = fix_char(to_insert[i])
            if processed_char == '{':    # case: invalid char
                continue
            next_element_tree = None
            for child in current_element_tree.children:
                if child.value == processed_char:
                    next_element_tree = child
                    break
            if next_element_tree is None:
                next_element_tree = Node(processed_char)
                current_element_tree.children.append(next_element_tree)
            if i == length_word - 1:
                next_element_tree.inc_end_of_word()
            current_element_tree = next_element_tree

    def find(self, to_find: string):
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


def fix_char(char) -> string:
    ord_char = ord(char)
    if char.isalpha():
        if char.isupper():  # upper case
            char = char.lower()  # lowercase the uppercase letters
    else:
        char = '{'      # ord = 123
    return char


def somehow_print_tree(it: Node):
    print(f'curr: {it.value}, children: ', end=' ')
    for child in it.children:
        print(f'{child.value}', end=', ')
    if it.numberOfEndOfWord > 0:
        print(it.numberOfEndOfWord)
    else:
        print('')

    if len(it.children) > 0:
        for ch in it.children:
            somehow_print_tree(ch)


def dfs(node: Node, st: string) -> list[str]:
    li = []
    st = st + node.value
    for i in range(node.numberOfEndOfWord):
        li.append(st)
    for child in node.children:
        li.extend(dfs(child, st))
    return li


def answer_a_query(tree_n: Tree, tree_r: Tree, pattern: string, list_words: list[str]):
    # extract letters into two parts -> p1:(before '\S*') p2:(after '\S*')
    parts: list[str]
    parts = pattern.split('\\S*')
    # lower case letters of each part
    parts[0].lower()
    parts[1].lower()
    # reverse second part
    parts[1] = parts[1][::-1]
    # last letters of each substring
    last_letter_normal: Node
    last_letter_reversed: Node
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
        print(0)
    else:
        list_normal = []
        list_reversed = []

        if last_letter_normal.value != '-1' and last_letter_reversed.value != '-1':
            list_normal = dfs(last_letter_normal, parts[0][0:len(parts[0]) - 1:])
            list_reversed = dfs(last_letter_reversed, parts[1][0:len(parts[1]) - 1:])
            list_final = []

            for st in list_normal:
                if (st[::-1] in list_reversed) and (len(st) >= len(parts[0]) + len(parts[1])):
                    list_final.append(st)
            print(len(list_final), end=' ')
            for st in list_final:
                print(st, end=' ')
            print('')  # end line
            return

        elif last_letter_normal.value != '-1' and last_letter_reversed.value == '-1':
            list_normal = dfs(last_letter_normal, parts[0][0:len(parts[0]) - 1:])
            print(len(list_normal), end=' ')
            for st in list_normal:
                print(st, end=' ')
            print('')  # end line
            return

        elif last_letter_normal.value == '-1' and last_letter_reversed.value != '-1':
            list_reversed = dfs(last_letter_reversed, parts[1][0:len(parts[1]) - 1:])
            print(len(list_reversed), end=' ')
            for st in list_reversed:
                print(st[::-1], end=' ')
            print('')  # end line
            return

        else:
            print(len(list_words), end=' ')
            for st in list_words:
                print(st, end=' ')
            print('')  # end line
            return


def main():
    # inputting values
    n, q = map(int, input().split())
    words = list((input().strip().split(' ')))

    queries = []
    for i in range(q):
        queries.append(input().strip())

    # preprocess and organization of data
    # one tree without reversing the words:
    tree_normal = Tree()
    for word in words:
        tree_normal.insert(word)
    tree_reversed = Tree()
    for word in words:
        tree_reversed.insert(word[::-1])

    # answering queries
    for i, query in enumerate(queries):
        answer_a_query(tree_normal, tree_reversed, query, words)


if __name__ == '__main__':
    main()
