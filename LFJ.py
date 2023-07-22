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
        result = check_first_elements_equal(relations)
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
        s = []
        s.append(self.leapfrog_init())
        while not self.atEnd:
            s.append(self.leapfrog_next())
        s = s[1:len(s) - 1]
        if self.spe is not None:
            s = [self.spe] + s
        return s


A = [0, 1, 2, 3]
B = [0, 1, 2]


lfj = LeapfrogJoin([A, B])
print(lfj.result())
