# coding: utf-8

__author__ = 'qinanlan <qinanlan@domob.com>'

import sys
content = sys.stdin.readlines()
P, Q, N = [i for i in content[0].split()]

P = float(P/100)
Q = float(Q/100)


class Node(object):
    def __init__(self, is_item, item_index, children=None):
        self.is_item = is_item
        self.item_index = item_index
        self.children = {} if children is None else children

class Tree(object):
    def __init__(self):
        first_child = {
            P: Node(True, 1),
            1-P: Node(False, 0)
        }
        self.root = Node(False, 0, first_child)

def solution():
    tree = Tree()
    pros = []
    result = [0]
    res = []

    def gen_tree(current_node):
        for key, value in current_node.children.items():
            if value.item_index == N:
                continue
            if value.is_item:
                value.children = {
                    P/pow(2, value.item_index): Node(True, value.item_index+1),
                    1-P/pow(2, value.item_index): Node(False, value.item_index)
                }
                gen_tree(value)
            else:
                pro = 1 if key+Q > 1 else key+Q
                value.children = {
                    pro: Node(True, value.item_index+1)
                }
                if pro < 1:
                    value.children[1-(pro)] = Node(False, value.item_index)
                gen_tree(value)
    def query(node):
        for key, value in node.children.items():
            pros.append(key)
            if value.item_index == N:
                for pp in pros:
                    result[0] += pp
                res.append(round(float(result[0]), 2))
                pros.pop()
                result[0] = 0
            else:
                query(value)
    gen_tree(tree.root)
    query(tree.root)
    final_res = 0
    for rr in res:
        final_res += rr
    print final_res
    return 0

solution()