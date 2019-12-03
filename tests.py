from RTree import RTree
from GreeneTree import GreeneTree
from Obj import Obj
from MBR import MBR
from Coordinate import Coordinate
from random import randint
import time
from statistics import mean


def main():
    # basic_demo()
    # insertion_demo(1000, 64, 32)
    wasted_space_demo(1000, 4, 2)
    return


def basic_demo():
    r_tree = RTree(4, 2)
    g_tree = GreeneTree(4, 2)

    coords = [Obj("R", MBR(Coordinate(20, 45), Coordinate(30, 20))),
                Obj('A', MBR(Coordinate(22, 40), Coordinate(30, 30))),
                Obj('B', MBR(Coordinate(25, 35), Coordinate(40, 25))),
                Obj('C', MBR(Coordinate(44, 40), Coordinate(47, 25))),
                Obj('D', MBR(Coordinate(52, 43), Coordinate(68, 22))),
                Obj('E', MBR(Coordinate(13, 45), Coordinate(20, 25))),
                Obj('F', MBR(Coordinate(34, 44), Coordinate(42, 37))),
                Obj('G', MBR(Coordinate(7, 24), Coordinate(13, 12))),
                Obj('H', MBR(Coordinate(22, 45), Coordinate(24, 27))),
                Obj('I', MBR(Coordinate(44, 41), Coordinate(47, 35))),
                Obj('J', MBR(Coordinate(2, 27), Coordinate(11, 17))),
                Obj('K', MBR(Coordinate(72, 27), Coordinate(81, 17))),
                Obj('L', MBR(Coordinate(66, 47), Coordinate(71, 37))),
                Obj('M', MBR(Coordinate(56, 53), Coordinate(76, 46))),
                Obj('N', MBR(Coordinate(77, 22), Coordinate(88, 15))),
                Obj('O', MBR(Coordinate(67, 47), Coordinate(78, 37)))]

    for i in coords:
        r_tree.insert(i)
        g_tree.insert(i)

    r_tree.draw()
    g_tree.draw()
    print("RTree:")
    print(r_tree)
    print("Greene Tree:")
    print(g_tree)

    return


def insertion_demo(n, max, min):
    coords = set()

    def generate_coords(n):
        for i in range(n):
            x1 = randint(0, 995)
            y1 = randint(0, 595)
            x2 = randint(x1 + 1, 1000)
            y2 = randint(y1 + 1, 600)
            rect = Obj("", MBR(Coordinate(x1, y2), Coordinate(x2, y1)))
            rect.val = str(id(rect))
            coords.add(rect)
        return

    r_times = list()
    g_times = list()
    for t in range(10):
        generate_coords(n)
        r_tree = RTree(max, min)
        g_tree = GreeneTree(max, min)

        start_time = time.time()
        for i in coords:
            r_tree.insert(i)
        r_times.append(time.time() - start_time)

        start_time = time.time()
        for i in coords:
            g_tree.insert(i)
        g_times.append(time.time() - start_time)

    print("{} insertions into r_tree: {} average".format(n, mean(r_times)))
    print("{} insertions into g_tree: {} average".format(n, mean(g_times)))

    return


def wasted_space_demo(n, max, min):
    coords = set()

    def generate_coords(n):
        for i in range(n):
            x1 = randint(0, 995)
            y1 = randint(0, 595)
            x2 = randint(x1 + 1, 1000)
            y2 = randint(y1 + 1, 600)
            rect = Obj("", MBR(Coordinate(x1, y2), Coordinate(x2, y1)))
            rect.val = str(id(rect))
            coords.add(rect)
        return

    r_wasted = list()
    g_wasted = list()

    for t in range(10):
        generate_coords(n)
        r_tree = RTree(max, min)
        g_tree = GreeneTree(max, min)

        for i in coords:
            r_tree.insert(i)
        wasted_space = r_tree.root.mbr.area - (r_tree.root.children[0].mbr.area + r_tree.root.children[1].mbr.area -
                                           r_tree.root.children[0].mbr.overlap(r_tree.root.children[1].mbr))
        r_wasted.append(wasted_space)

        for i in coords:
            g_tree.insert(i)
        wasted_space = g_tree.root.mbr.area - (g_tree.root.children[0].mbr.area + g_tree.root.children[1].mbr.area -
                                           g_tree.root.children[0].mbr.overlap(g_tree.root.children[1].mbr))
        g_wasted.append(wasted_space)

    print("average wasted space r_tree: {}".format(mean(r_wasted)))
    print("average wasted space g_tree: {}".format(mean(g_wasted)))

    return

if __name__ == '__main__':
    main()
