import copy
import profile
import random
import time
from memory_profiler import profile


class LinearIterator:
    def __init__(self, relation):
        self.relation = relation
        self.index = 0

    def key(self):
        return self.relation[self.index]

    def next(self):
        if not self.atEnd():
            self.index += 1

    def seek(self, seekKey):
        if seekKey > self.relation[-1]:
            self.index = len(self.relation)
            return
        while self.key() < seekKey:
            self.next()

    def atEnd(self):
        return self.index >= len(self.relation)


def check_first_elements_equal(lists):
    first_elements = [l[0] for l in lists]
    return len(set(first_elements)) == 1


class LeapfrogJoin:
    def __init__(self, relations):
        self.relations = relations
        result = check_first_elements_equal(relations)
        self.spe = None
        if result:
            self.spe = relations[0][0]
        self.iterators = [LinearIterator(relation) for relation in relations]
        self.atEnd = any(iterator.atEnd() for iterator in self.iterators)
        self.p = 0

    def leapfrog_init(self):
        if self.atEnd or any(iterator.atEnd() for iterator in self.iterators):
            return []
        self.iterators.sort(key=lambda iterator: iterator.key())
        self.p = 0
        return self.leapfrog_search

    def leapfrog_search(self):
        x_prime = self.iterators[(self.p - 1) % len(self.iterators)].key()
        res = None
        while not self.atEnd:
            x = self.iterators[self.p].key()
            if x == x_prime:
                self.key = x
                res = x
                break
            else:
                self.iterators[self.p].seek(x_prime)
                if self.iterators[self.p].atEnd():
                    self.atEnd = True
                    break
                else:
                    x_prime = self.iterators[self.p].key()
                    self.p = (self.p + 1) % len(self.iterators)
        return res

    def leapfrog_next(self):
        self.iterators[self.p].next()
        if self.iterators[self.p].atEnd():
            self.atEnd = True
        else:
            self.p = (self.p + 1) % len(self.iterators)
        return self.leapfrog_search()

    def leapfrog_seek(self, seekKey):
        self.iterators[self.p].seek(seekKey)
        if self.iterators[self.p].atEnd():
            self.atEnd = True
        else:
            self.p = (self.p + 1) % len(self.iterators)
        return self.leapfrog_search()

    def result(self):
        if len(self.relations) == 1:
            return self.relations[0]
        s = []
        s.append(self.leapfrog_init())
        while not self.atEnd:
            s.append(self.leapfrog_next())
        s = s[1: len(s) - 1]
        if self.spe is not None:
            s = [self.spe] + s
        return s


class TrieNode:
    def __init__(self, key, parent):
        self.key = key
        self.parent = parent
        self.children = {}
        self.visited = False

    def addChildren(self, key):
        if key not in self.children:
            self.children[key] = TrieNode(key, self)

    def getChildren(self):
        return self.children

    def getParent(self):
        return self.parent

    def getKey(self):
        return self.key

    def isLeaf(self):
        return len(self.children) == 0


class TrieIterator:
    def __init__(self, relation):
        self.root = TrieNode(None, None)
        self.relation = relation
        self.itr = None
        self.tree = self.buildTrie()
        self.atEnd = False

    def buildTrie(self):
        cRelation = [list(d.values()) for d in self.relation]
        for key in cRelation:
            node = self.root
            for el in key:
                if el not in node.getChildren():
                    node.addChildren(el)
                node = node.getChildren()[el]
        self.itr = self.root
        return self.root

    def open(self):
        curr = self.itr
        if curr.getChildren():
            curr = curr.getChildren()[list(curr.getChildren())[0]]
        self.itr = curr

    def next(self):
        curr = self.itr
        if curr.parent:
            child_index = list(curr.parent.getChildren()).index(curr.getKey())
            if child_index < len(curr.parent.getChildren()) - 1:
                next_child_key = list(curr.parent.getChildren())[
                    child_index + 1]
                self.itr = curr.parent.getChildren()[next_child_key]
            else:
                self.atEnd = True
        else:
            return

    def up(self):
        curr = self.itr
        if curr.getParent():
            curr = curr.getParent()
        self.itr = curr
        if self.atEnd:
            self.atEnd = False


class LeapfrogJoinTrie:
    def __init__(self, relations):
        self.output = []
        self.depth = -1
        sortedRelations = []
        for rel in relations:
            sortKey = list(rel[0].keys())
            rel = sorted(rel, key=lambda x: tuple(x[key] for key in sortKey))
            sortedRelations.append(rel)
        attS = set()
        for rel in relations:
            for att in rel:
                attS.update(att)
        attS.discard("name")
        self.attributes = list(attS)
        self.attributes.sort()
        self.tries = [TrieIterator(relation) for relation in sortedRelations]
        self.arr = []
        for att in self.attributes:
            smallArr = []
            for itr in self.tries:
                if att in itr.relation[0]:
                    smallArr.append(itr)
            self.arr.append(smallArr)

    def open(self):
        self.depth += 1
        for itr in self.arr[self.depth]:
            itr.open()

    def up(self):
        for itr in self.arr[self.depth]:
            itr.up()
        self.depth -= 1

        
            

    def result(self):
        self.resultH([])
        return self.output
    @profile
    def resultH(self, t):
        b = False
        while True:
            if self.depth == len(self.arr) - 1:
                leap = []
                for ele in self.arr[self.depth]:
                    sing = []
                    while not ele.atEnd:
                        sing.append(ele.itr.getKey())
                        ele.next()
                    leap.append(sing)
                lp = LeapfrogJoin(leap)
                for i in lp.result():
                    t.append(i)
                    self.output.append(t)
                    t = t[:-1]
                self.up()
            if self.arr[self.depth][0].atEnd and self.arr[self.depth][0].itr.visited:
                if t:
                    t.pop()
                self.up()
            if not self.arr[self.depth][0].atEnd and self.arr[self.depth][0].itr.visited:
                self.arr[self.depth][0].next()
                main = self.arr[self.depth][0].itr.getKey()
                for itr in self.arr[self.depth]:
                    while not itr.itr.getKey() == main and not itr.atEnd:
                        itr.next()
                    if itr.atEnd and itr.itr.getKey() != main:
                        self.arr[self.depth][0].next()
                        if self.arr[self.depth][0].atEnd:
                            if t:
                                t.pop()
                            self.up()
                            b = True
                            break
                if b:
                    b = False
                    continue
                if t:
                    t.pop()
                val = self.arr[self.depth][0].itr.getKey()
                t.append(val)
                if t[0] is None:
                    break
            if self.arr[self.depth][0].atEnd and self.arr[self.depth][0].itr.visited and self.depth == 0:
                break
            if not self.arr[self.depth][0].itr.visited:
                self.arr[self.depth][0].itr.visited = True
                main = self.arr[self.depth][0].itr.getKey()
                for itr in self.arr[self.depth]:
                    while not itr.itr.getKey() == main and not itr.atEnd:
                        itr.next()
                    if itr.atEnd and itr.itr.getKey() != main:
                        self.arr[self.depth][0].next()
                        if self.arr[self.depth][0].atEnd:
                            if t:
                                t.pop()
                            self.up()
                            b = True
                            break
                if b:
                    b = False
                    continue
                self.open()
                if not self.depth == len(self.arr) - 1:
                    val = self.arr[self.depth][0].itr.getKey()
                    t.append(val)
                    if t[0] is None:
                        break


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


def generate_random_list(num_dicts, num_attributes):

    wholeList = []

    for _ in range(random.randint(1, 5)):

        random_list = []
        attributelist = [random.randint(1, 5) for _ in range(num_attributes)]
        attributelist.sort()

        for _ in range(num_dicts):
            new_dict = {}

            attribute_name = 'attribute_'
            for i in range(len(attributelist)):
                attribute_value = random.randint(1, 3)

                new_dict[attribute_name +
                         str(attributelist[i]+1)] = attribute_value

            random_list.append(new_dict)
        wholeList.append(random_list)

    return wholeList


R = [

    {'a': 1, 'b': 'abc', 'd': 4.5},
    {'a': 2, 'b': 'def', 'd': 6.7},
    {'a': 3, 'b': 'ghi', 'd': 2.1},
    {'a': 4, 'b': 'jkl', 'd': 8.9},


]


S = [

    {'b': 'abc', 'c': 10},
    {'b': 'def', 'c': 20},
    {'b': 'mno', 'c': 30},

]

T = [

    {'c': 10, 'd': 4.5},
    {'c': 20, 'd': 6.7},
    {'c': 40, 'd': 2.1},

]

H = [
    {'a': 1, 'e': 1},
    {'a': 2,   'e': 2},
    {'a': 5,   'e': 3},
    {'a': 7,   'e': 4},
]

G = [
    {'e': 1, 'f': 1},
    {'e': 2, 'f': 2},
    {'e': 3, 'f': 3},
]


relations = [R, S, T, H, G]

# relations = generate_random_list(6, 6)
print(relations)
print()

brforeTime = time.time()
Leap = LeapfrogJoinTrie(relations)
print('Trie join ----> ', Leap.result())
afterTime = time.time()
print(afterTime - brforeTime)


print()
before2 = time.time()
print('Binary Join result ------>', join(relations))
after2 = time.time()
print(after2 - before2)
