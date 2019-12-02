from MBR import MBR
from Drawer import Drawer
import queue

class RTree:
    def __init__(self, maxN, minN):
        self.root = None
        self.maxN = maxN
        self.minN = minN
        self.drawer = Drawer(self)

    def draw(self):
        self.drawer.draw()

    def __repr__(self):
        output = str(self.root.mbr) + "|"
        q = queue.Queue()
        q2 = queue.Queue()
        q.put(self.root)
        while not q.empty():
            u = q.get()
            for idx, i in enumerate(u.members):
                if (idx + 1) < len(u.members):
                    try:
                        output = output + i.val + ","
                    except:
                        output = output + str(i) + ","
                elif not q.empty():
                    try:
                        output = output + i.val + ":"
                    except:
                        output = output + str(i) + ":"
                else:
                    try:
                        output = output + i.val
                    except:
                        output = output + str(i)
            for idx, i in enumerate(u.children):
                q2.put(i)
            if q.empty():
                if not q2.empty():
                    output = output + "|"
                while not q2.empty():
                    q.put(q2.get())
        return output

    def insert(self, obj):
        '''
        insert new object into RTree
        :param obj: object to insert
        :return:
        '''
        if self.root is None:
            self.root = self.Node(MBR.generate(obj.mbr), self.maxN, self.minN)
        self.root.insert(obj)


    def search(self, obj):
        '''
        search for the mbr containing a given object
        :param obj: object to search for
        :return: mbr containing that object
        '''
        node = self.root
        for i in node.children:
            if i.mbr.contains(obj.mbr):
                node = i
        return node

    class Node:
        def __init__(self, mbr=None, maxN=None, minN=None):
            self.parent = None
            self.children = list()
            self.members = list()
            self.mbr = mbr
            self.maxN = maxN
            self.minN = minN

        def insert(self, obj=None):
            '''
            insert new object into node
            :param obj: object to insert
            :return:
            '''
            for i in self.children:
                if i.mbr.contains(obj.mbr):
                    i.insert(obj)
                    return
                else:
                    node = self.find_min(self.children, obj)
                    node.mbr.resize(obj.mbr)
                    node.insert(obj)
                    return

            if len(self.members) < self.maxN:
                self.members.append(obj)
                self.mbr.resize(obj.mbr)
                node = self.parent
                while node != None:
                    node.mbr.resize(obj.mbr)
                    node = node.parent
                return

            if len(self.members) == self.maxN:
                self.members.append(obj)
                u, v = self.split()
                u.parent = self.parent
                v.parent = self.parent
                self.parent.children.extend([u, v])
                self.parent.children.remove(self)
                self.parent.members.extend([u.mbr, v.mbr])

                self.mbr.resize(v.mbr)
                node = self.parent
                while node != None:
                    node.mbr.resize(v.mbr)
                    node = node.parent
                return

            return

        def split(self):
            '''
            split node if capacity is reached
            :return: node a, b split from original
            '''
            d, x, y = -1, None, None
            for i in range(len(self.members)):
                for j in range(len(self.members)):
                    if i != j:
                        k = (self.members[i].mbr.euclidian_distance_rect(self.members[j].mbr))
                        if k > d:
                            d = k
                            x = self.members[i]
                            y = self.members[j]

            r = self.__class__(MBR.generate(x.mbr), self.maxN, self.minN)
            r.insert(x)
            s = self.__class__(MBR.generate(y.mbr), self.maxN, self.minN)
            s.insert(y)

            m = [i for i in self.members if i != x and i != y]
            for i in range(len(m)):
                count = len(m) - i
                rthresh = r.minN - len(r.members)
                sthresh = s.minN - len(s.members)
                if count == rthresh:
                    r.insert(m[i])
                elif count == sthresh:
                    s.insert(m[i])
                else:
                    n = self.find_min([r, s], m[i])
                    n.insert(m[i])

            for i in [r, s]:
                for j in range(len(i.members)):
                    if not i.mbr.contains(i.members[j].mbr):
                        i.mbr.resize(i.members[j].mbr)
            return r, s

        @staticmethod
        def find_min(nodes, insertion):
            """
            Find the node most optimal for insertion
            :param rt_nodes:
            :param entry:
            :return:
            """
            e = []
            for i in range(len(nodes)):
                if nodes[i].mbr.contains(insertion.mbr):
                    v = 0
                else:
                    v = MBR.generate2(nodes[i].mbr, insertion.mbr).area - nodes[i].mbr.area
                e.append({'node': nodes[i], 'expanded': v})
            return min(e, key=lambda x: x['expanded'])['node']
