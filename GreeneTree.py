from MBR import MBR
from Drawer import Drawer
import queue
import math

class GreeneTree:
    def __init__(self, maxN, minN):
        self.root = None
        self.maxN = maxN
        self.minN = minN
        self.drawer = Drawer(self)

    def draw(self):
        self.drawer.draw()

    def __repr__(self):
        output = str(self.root) + "|"
        q = queue.Queue()
        q2 = queue.Queue()
        q.put(self.root)
        while not q.empty():
            u = q.get()
            if u.depth != 1:
                for idx, i in enumerate(u.children):
                    if (idx + 1) < len(u.children):
                        output = output + str(i) + ","
                    elif not q.empty():
                        output = output + str(i) + ":"
                    else:
                        output = output + str(i)
                for idx, i in enumerate(u.children):
                    q2.put(i)
            else:
                for idx, i in enumerate(u.children):
                    if (idx + 1) < len(u.children):
                        output = output + i.val + ","
                    elif not q.empty():
                        output = output + i.val + ":"
                    else:
                        output = output + i.val
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
            self.root = self.Leaf(MBR.generate(obj.mbr), self.maxN, self.minN, 1)
            self.root.children.append(obj)
            return

        n = self.root
        while n.depth is not 1:
            for i in n.children:
                if i.mbr.contains(obj.mbr):
                    n = i
                    break
                else:
                    node = n.find_min(n.children, obj)
                    node.mbr.resize(obj.mbr)
                    n = node
                    break

        if len(n.children) < n.maxN:
            n.children.append(obj)
            while n is not None:
                n.mbr.resize(obj.mbr)
                n = n.parent
            return

        if len(n.children) == n.maxN:
            n.children.append(obj)
            self.overflow(n)
            while n is not None:
                n.mbr.resize(obj.mbr)
                n = n.parent
        return

    def overflow(self, n):
        u, v = n.split()

        n.mbr.resize(u.mbr)
        n.mbr.resize(v.mbr)

        if n == self.root:
            self.root = self.Branch(self.root.mbr, self.maxN, self.minN, n.depth + 1)
            self.root.children.extend([u, v])
            u.parent = self.root
            v.parent = self.root

        else:
            u.parent = n.parent
            v.parent = n.parent
            n.parent.children.remove(n)
            n.parent.children.extend([u, v])
            if len(n.parent.children) > self.maxN:
                self.overflow(n.parent)

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
        def __init__(self, mbr=None, maxN=None, minN=None, depth=None):
            self.parent = None
            self.children = list()
            self.mbr = mbr
            self.maxN = maxN
            self.minN = minN
            self.depth = depth

        def split(self):
            return None

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

    class Leaf(Node):
        def __init__(self, mbr=None, maxN=None, minN=None, depth=1):
            super().__init__(mbr, maxN, minN, depth)

        def split(self):
            '''
            split node if capacity is reached
            :return: node a, b split from original
            '''
            d, x, y = -1, None, None
            for i in range(len(self.children)):
                for j in range(len(self.children)):
                    if i != j:
                        k = (self.children[i].mbr.euclidian_distance_rect(self.children[j].mbr))
                        if k > d:
                            d = k
                            x = self.children[i]
                            y = self.children[j]

            left = x.mbr.lower_right.x < y.mbr.upper_left.x
            right = x.mbr.upper_left.x < y.mbr.lower_right.x
            bottom = x.mbr.upper_left.y < y.mbr.lower_right.y
            top = x.mbr.lower_right.y < y.mbr.upper_left.y

            if left and bottom:
                dist_x = y.mbr.lower_left.x - x.mbr.upper_right.x
                dist_y = y.mbr.lower_left.y - x.mbr.upper_right.y
            elif right and bottom:
                dist_x = x.mbr.lower_left.x - y.mbr.upper_right.x
                dist_y = y.mbr.lower_right.y - x.mbr.upper_left.y
            elif left and top:
                dist_x = y.mbr.lower_left.x - x.mbr.upper_right.x
                dist_y = x.mbr.lower_left.y - y.mbr.upper_right.y
            else:
                dist_x = x.mbr.lower_left.x - y.mbr.upper_right.x
                dist_y = x.mbr.lower_left.y - y.mbr.upper_right.y

            normalized_x = dist_x / (self.mbr.upper_right.x - self.mbr.upper_left.x)
            normalized_y = dist_y / (self.mbr.upper_right.y - self.mbr.lower_left.y)

            if normalized_x > normalized_y:
                sorted_children = sorted(self.children, key=lambda i: (i.mbr.lower_left.x + i.mbr.lower_right.x)/2)
            else:
                sorted_children = sorted(self.children, key=lambda i: (i.mbr.upper_left.y + i.mbr.lower_right.y) / 2)

            r = self.__class__(MBR.generate(x.mbr), self.maxN, self.minN, self.depth)
            s = self.__class__(MBR.generate(y.mbr), self.maxN, self.minN, self.depth)

            m = math.floor((self.maxN+1)/2)
            for i in sorted_children[:m]:
                r.children.append(i)
            for i in sorted_children[-m:]:
                s.children.append(i)
            if (self.maxN + 1) % 2 != 0:
                n = self.find_min([r, s], sorted_children[m])
                n.children.append(sorted_children[m])

            for i in [r, s]:
                for j in range(len(i.children)):
                    if not i.mbr.contains(i.children[j].mbr):
                        i.mbr.resize(i.children[j].mbr)

            return r, s

    class Branch(Node):
        def __init__(self, mbr=None, maxN=None, minN=None, depth=None):
            super().__init__(mbr, maxN, minN, depth)

        def split(self):
            '''
            split node if capacity is reached
            :return: node a, b split from original
            '''
            d, x, y = -1, None, None
            for i in range(len(self.children)):
                for j in range(len(self.children)):
                    if i != j:
                        k = (self.children[i].mbr.euclidian_distance_rect(self.children[j].mbr))
                        if k > d:
                            d = k
                            x = self.children[i]
                            y = self.children[j]

            left = x.mbr.lower_right.x < y.mbr.upper_left.x
            right = x.mbr.upper_left.x < y.mbr.lower_right.x
            bottom = x.mbr.upper_left.y < y.mbr.lower_right.y
            top = x.mbr.lower_right.y < y.mbr.upper_left.y

            if left and bottom:
                dist_x = y.mbr.lower_left.x - x.mbr.upper_right.x
                dist_y = y.mbr.lower_left.y - x.mbr.upper_right.y
            elif right and bottom:
                dist_x = x.mbr.lower_left.x - y.mbr.upper_right.x
                dist_y = y.mbr.lower_right.y - x.mbr.upper_left.y
            elif left and top:
                dist_x = y.mbr.lower_left.x - x.mbr.upper_right.x
                dist_y = x.mbr.lower_left.y - y.mbr.upper_right.y
            else:
                dist_x = x.mbr.lower_left.x - y.mbr.upper_right.x
                dist_y = x.mbr.lower_left.y - y.mbr.upper_right.y

            normalized_x = dist_x / (self.mbr.upper_right.x - self.mbr.upper_left.x)
            normalized_y = dist_y / (self.mbr.upper_right.y - self.mbr.lower_left.y)

            if normalized_x > normalized_y:
                sorted_children = sorted(self.children, key=lambda i: (i.mbr.lower_left.x + i.mbr.lower_right.x) / 2)
            else:
                sorted_children = sorted(self.children, key=lambda i: (i.mbr.upper_left.y + i.mbr.lower_right.y) / 2)

            r = self.__class__(MBR.generate(x.mbr), self.maxN, self.minN, self.depth)
            s = self.__class__(MBR.generate(y.mbr), self.maxN, self.minN, self.depth)

            m = math.floor((self.maxN + 1) / 2)
            for i in sorted_children[:m]:
                r.children.append(i)
            for i in sorted_children[-m:]:
                s.children.append(i)
            if (self.maxN + 1) % 2 != 0:
                n = self.find_min([r, s], sorted_children[m])
                n.children.append(sorted_children[m])

            for i in [r, s]:
                for j in range(len(i.children)):
                    i.children[j].parent = i
                    if not i.mbr.contains(i.children[j].mbr):
                        i.mbr.resize(i.children[j].mbr)

            return r, s
