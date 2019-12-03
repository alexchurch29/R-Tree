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
    wasted_space_demo(1000, 64, 32)
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

    def sweep(node):
        area = 0
        rectangles = [i.mbr for i in node.children]
        x_vals, y_vals = [], []

        for rectangle in rectangles:
            x_vals.extend([rectangle.lower_left.x, rectangle.lower_right.x])
            y_vals.extend([rectangle.lower_left.y, rectangle.upper_left.y])

        x_vals, y_vals = list(sorted(x_vals)), list(sorted(y_vals))

        for i in range(1, len(x_vals)):
            for j in range(1, len(y_vals)):
                cell = MBR(Coordinate(x_vals[i - 1], y_vals[j - 1]), Coordinate(x_vals[i], y_vals[j]))
                # print 'Checking cell', cell
                for rectangle in rectangles:
                    center = Coordinate((cell.lower_right.x + cell.upper_left.x)/2, (cell.lower_right.y + cell.upper_left.y)/2)
                    contains = rectangle.upper_left.y > center.y and rectangle.upper_left.x < center.x \
                        and rectangle.lower_right.y < center.y and rectangle.lower_right.x > center.x
                    if contains:
                        # print '\tAdding area', cell.area
                        area = area - cell.area
                        break

        return area

    generate_coords(n)
    r_tree = RTree(max, min)
    g_tree = GreeneTree(max, min)
    for i in coords:
        r_tree.insert(i)
        g_tree.insert(i)

    r_wasted = list()

    def wasted_space(node):
        while node.depth != 1:
            waste = node.mbr.area - sweep(node)
            r_wasted.append(waste / node.mbr.area)
            for j in node.children:
                node = j
                wasted_space(node)
        return

    wasted_space(r_tree.root)
    print("average wasted space r_tree: {}".format(1-mean(r_wasted)))

    g_wasted = list()

    def wasted_space(node):
        while isinstance(node, GreeneTree.Node):
            waste = node.mbr.area - sweep(node)
            g_wasted.append(waste / node.mbr.area)
            for j in node.children:
                node = j
                wasted_space(node)
        return

    wasted_space(g_tree.root)
    print("average wasted space r_tree: {}".format(1-mean(g_wasted)))

    return

if __name__ == '__main__':
    main()
