
import random
import time
import pandas as pd
import math
from memory_profiler import profile


class Node:
    def __init__(self):
        self.value = None
        self.left = None
        self.right = None
        self.label = set()
        self.isLeaf = False


class BinaryTree:
    def __init__(self, variables):
        self.root = self.buildTree(variables, variables, variables)

    def buildTree(self, variables, labels, Allvariables):
        if len(variables) == 1:
            node = Node()
            node.label = [d for d in Allvariables if d not in variables]
            node.value = variables[0]
            node.isLeaf = True
            return node

        node = Node()
        if not node.isLeaf:
            node.label = [d for d in Allvariables if d not in variables]
        while True:
            index = random.randint(1, len(variables))
            first_half = variables[:index]
            second_half = variables[index:]
            if first_half and second_half:
                break
        firstLabel = [d for d in labels if d not in first_half]
        secondLabel = [d for d in labels if d not in second_half]
        node.left = self.buildTree(first_half, firstLabel, Allvariables)
        node.right = self.buildTree(second_half, secondLabel, Allvariables)
        return node

    def printTree(self):
        self.printTreeHelper(self.root, 0)
        print()
        self.printTreeHelperW(self.root, 0)

    def printTreeHelper(self, node, level):
        if node is None:
            return
        self.printTreeHelper(node.right, level+1)
        print("    "*level, end="")
        print(node.label)
        if node.value is not None:
            print(node.value)
        else:
            print("X")
        self.printTreeHelper(node.left, level+1)

    def printTreeHelperW(self, node, level):
        if node is None:
            return
        self.printTreeHelperW(node.right, level+1)
        print("    "*level, end="")
        if node.value is not None:
            print(node.value)
        else:
            print("X")
        self.printTreeHelperW(node.left, level+1)

    def LW(self, attributes, relations):
        n = len(attributes)
        num = 1
        for d in relations:
            num *= len(d)
        P = num ** (1/(n-1))
        # print(P)
        curr = self.root
        root_c, root_d = self.LWHelper(curr, P, relations)
        print("Result --> ", root_c)

    def projectData(self, attributes, relations):
        return [{attr: d[attr] for attr in attributes} for d in relations if all(key in d for key in attributes)]

    def LWHelper(self, node, P, relations):
        if node.isLeaf:
            for relation in relations:
                if all(key in relation[0] for key in node.label):
                    return [], relation

        cl, dl = self.LWHelper(node.left, P, relations)
        cr, dr = self.LWHelper(node.right, P, relations)

        leftP = self.projectData(node.label, dl)
        rightP = self.projectData(node.label, dr)

        f = [d for d in leftP if d in rightP]
        g = [t for t in f if countT(dl, t)+1 <= math.ceil(P/len(dr))]
        print(g)

        common_keys = set()
        kl = None
        kr = None

        # if node.left.isLeaf:
        #     kl = dl
        # else:
        #     kl = cl

        # if node.right.isLeaf:
        #     kr = dr
        # else:
        #     kr = cr

        for dict1 in dl:
            for dict2 in dr:
                common_keys.update(dict1.keys() & dict2.keys())

        joined_list = []
        for dict1 in dl:
            for dict2 in dr:
                if all(dict1.get(key) == dict2.get(key) for key in common_keys):
                    joined_dict = {}
                    for key in common_keys:
                        if dict1.get(key) == dict2.get(key):
                            joined_dict.update(dict1)
                            joined_dict.update(dict2)
                    if joined_dict:
                        joined_list.append(joined_dict)

        if node == self.root:
            for item in cr + cl:
                if item not in joined_list:
                    joined_list.append(item)
            c = joined_list
            d = []
        else:
            for item in cr + cl:
                if item not in joined_list:
                    joined_list.append(item)
            c = joined_list
            d = [j for j in f if j not in g]
        return c, d


def generateData():
    num_variables = 14

    keys = [chr(ord('A') + i) for i in range(num_variables)]

    list_of_lists = []
    for i in range(num_variables):
        sublist = []
        for j in range(random.randint(1, 3)):
            dictionary = {}
            for k in range(num_variables - 1):
                key = keys[(i + k) % num_variables]
                value = random.randint(1, 3)
                dictionary[key] = value
            sublist.append(dictionary)
        list_of_lists.append(sublist)
    return keys, list_of_lists


def countT(rel, t):
    count = 0
    for d in rel:
        if all(d.get(key) == t.get(key) for key in t.keys()):
            count += 1
    return count


def semiJoin(R, S):
    commonAttributes = None
    if R and S:
        commonAttributes = R[0].keys() & S[0].keys()
    else:
        return []
    result = []
    for tupleR in R:
        for tupleS in S:
            if all(tupleR.get(key) == tupleS.get(key) for key in commonAttributes):
                newTuple = {}
                newTuple.update(tupleR)
                result.append(newTuple)
    return result


def joinTwoRelations(R, S):
    '''Joins two relations using the traditional join algorithm'''
    commonAttributes = None
    if R and S:
        commonAttributes = R[0].keys() & S[0].keys()
    else:
        return []
    result = []
    for tupleR in R:
        for tupleS in S:
            if all(tupleR.get(key) == tupleS.get(key) for key in commonAttributes):
                newTuple = {}
                newTuple.update(tupleR)
                newTuple.update(tupleS)
                result.append(newTuple)
    return result


def join(relationsList):
    '''Joins a list of relations using the traditional join algorithm'''
    # Get the first relation in the list
    result = relationsList[0]
    # For each relation in the list
    for relation in relationsList[1:]:
        # Join the current result with the current relation
        result = joinTwoRelations(result, relation)
    # Return the result
    return result


# R = [{'A': 'Youssef', 'B': 22}, {
#     'A': 'sara', 'B': 23}, {'A': 'marselle', 'B': 74}]
# S = [{'B': 4, 'C': 'Toddler'}, {'B': 14, 'C': 'Teen'}, {
#     'B': 22, 'C': 'Adult'}, {'B': 74, 'C': 'OLD'}]
# T = [{'C': 'Adult', 'A': 'Youssef'}, {'C': 'OLD',
#                                       'A': 'marselle'}, {'C': 'Toddler', 'A': 'kiro'}]
# R = [
#     {"a": 7, "b": 50},
#     {"a": 7, "b": 51},
#     {"a": 7, "b": 52},
#     {"a": 7, "b": 53},
#     {"a": 7, "b": 54},
#     {"a": 7, "b": 55},
#     {"a": 7, "b": 56},
#     {"a": 7, "b": 57},
#     {"a": 7, "b": 58},
#     {"a": 7, "b": 59},
#     {"a": 7, "b": 60},
#     {"a": 7, "b": 61},
#     {"a": 7, "b": 62},
#     {"a": 7, "b": 63},
#     {"a": 7, "b": 64},
#     {"a": 7, "b": 65},
#     {"a": 7, "b": 66},
#     {"a": 7, "b": 67},
#     {"a": 7, "b": 68},
#     {"a": 7, "b": 69},
#     {"a": 7, "b": 70},
#     {"a": 7, "b": 71},
#     {"a": 7, "b": 72},
#     {"a": 7, "b": 73},
#     {"a": 7, "b": 74},
#     {"a": 7, "b": 75},
#     {"a": 7, "b": 76},
#     {"a": 7, "b": 77},
#     {"a": 7, "b": 78},
#     {"a": 7, "b": 79},
#     {"a": 7, "b": 80},
#     {"a": 7, "b": 81},
#     {"a": 7, "b": 82},
#     {"a": 7, "b": 83},
#     {"a": 7, "b": 84},
#     {"a": 7, "b": 85},
#     {"a": 7, "b": 86},
#     {"a": 7, "b": 87},
#     {"a": 7, "b": 88},
#     {"a": 7, "b": 89},
#     {"a": 7, "b": 90},
#     {"a": 7, "b": 91},
#     {"a": 7, "b": 92},
#     {"a": 7, "b": 93},
#     {"a": 7, "b": 94},
#     {"a": 7, "b": 95},
#     {"a": 7, "b": 96},
#     {"a": 7, "b": 97},
#     {"a": 7, "b": 98},
#     {"a": 7, "b": 99},

# ]

# S = [
#     {"b": 50, "c": 0},
#     {"b": 50, "c": 1},
#     {"b": 68, "c": 4},
#     {"b": 68, "c": 5},
#     {"b": 68, "c": 6},
#     {"b": 68, "c": 7},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 68, "c": 5},
#     {"b": 68, "c": 6},
#     {"b": 68, "c": 7},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 68, "c": 5},
#     {"b": 68, "c": 6},
#     {"b": 68, "c": 7},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 68, "c": 5},
#     {"b": 68, "c": 6},
#     {"b": 68, "c": 7},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 68, "c": 5},
#     {"b": 68, "c": 6},
#     {"b": 68, "c": 7},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 68, "c": 5},
#     {"b": 68, "c": 6},
#     {"b": 68, "c": 7},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 68, "c": 5},
#     {"b": 68, "c": 6},
#     {"b": 68, "c": 7},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 74, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 75, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},
#     {"b": 70, "c": 8},
#     {"b": 70, "c": 9},


#     {"b": 70, "c": 9},


# ]

# T = [
#     {"a": 7, "c": 0},
#     {"a": 7, "c": 1},
#     {"a": 7, "c": 2},
#     {"a": 7, "c": 3},
#     {"a": 7, "c": 4},
#     {"a": 7, "c": 5},
#     {"a": 7, "c": 6},
#     {"a": 7, "c": 7},
#     {"a": 7, "c": 8},
#     {"a": 7, "c": 9},
#     {"a": 7, "c": 10},
#     {"a": 7, "c": 11},
#     {"a": 7, "c": 12},
#     {"a": 7, "c": 13},
#     {"a": 7, "c": 14},
#     {"a": 7, "c": 15},
#     {"a": 7, "c": 16},
#     {"a": 7, "c": 17},
#     {"a": 7, "c": 18},
#     {"a": 7, "c": 19},
#     {"a": 7, "c": 20},
#     {"a": 7, "c": 21},
#     {"a": 7, "c": 22},
#     {"a": 7, "c": 23},
#     {"a": 7, "c": 24},
#     {"a": 7, "c": 25},
#     {"a": 7, "c": 26},
#     {"a": 7, "c": 27},
#     {"a": 7, "c": 28},
#     {"a": 7, "c": 29},
#     {"a": 7, "c": 30},
#     {"a": 7, "c": 31},
#     {"a": 7, "c": 32},
#     {"a": 7, "c": 33},
#     {"a": 7, "c": 34},
#     {"a": 7, "c": 35},
#     {"a": 7, "c": 36},
#     {"a": 7, "c": 37},
#     {"a": 7, "c": 38},

# ]

# R = [


# ]


# for i in range(10000):
#     R.append({'a': 7, 'b':  random.randint(0, 10000)})

# S = [

# ]

# for i in range(10000):
#     S.append({'b': random.randint(0, 10000), 'c': random.randint(0, 10000)})

# T = [

# ]

# for i in range(10000):
#     T.append({'a': 7, 'c': random.randint(0, 10000)})

# G = []
# for i in range(10000):
#     G.append({'a': 7, 'b': 4, 'd': random.randint(0, 10000)})
# R = [
#     {"a": 0, "b": 0},
#     {"a": 0, "b": 1},
#     {"a": 0, "b": 2},
#     {"a": 1, "b": 0},
#     {"a": 2, "b": 0},
# ]

# S = [
#     {"b": 0, "c": 0},
#     {"b": 0, "c": 1},
#     {"b": 0, "c": 2},
#     {"b": 1, "c": 0},
#     {"b": 2, "c": 0},
# ]
# T = [
#     {"a": 0, "c": 0},
#     {"a": 0, "c": 1},
#     {"a": 0, "c": 2},
#     {"a": 1, "c": 0},
#     {"a": 2, "c": 0},
# ]
R = [
    {"a": 7, "b": 4},

]


S = [
    {"b": 4, "c": 1},
    {"b": 4, "c": 3},
    {"b": 4, "c": 5},
    {"b": 4, "c": 9},
]

T = [
    {"a": 7, "c": 0},
    {"a": 7, "c": 2},
    {"a": 7, "c": 5},
    {"a": 7, "c": 7},
]


attributes = ['a', 'b', 'c']
relationsList = [R, S, T]

# attributes, relationsList = generateData()
# print(relationsList)

timeJoinBefore = time.time()
print('Join result ---- > ', join(relationsList))
join(relationsList)
timeJoinAfter = time.time()

print("Time Join: ", timeJoinAfter - timeJoinBefore)

timeBefore = time.time()
tree = BinaryTree(attributes)
tree.printTree()
tree.LW(attributes, relationsList)
timeAfter = time.time()

print("Time LW: ", timeAfter - timeBefore)
