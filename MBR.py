from Coordinate import Coordinate
from copy import deepcopy


class MBR:
    '''
    Minimum bounding rectangle in the 2d plane
    '''
    def __init__(self, upper_left=None, lower_right=None):
        self.upper_left = upper_left
        self.lower_right = lower_right
        self.upper_right = Coordinate(self.lower_right.x, self.upper_left.y)
        self.lower_left = Coordinate(self.upper_left.x, self.lower_right.y)
        self.area = (self.upper_right.x - self.upper_left.x) * (self.upper_left.y - self.lower_left.y)

    def __eq__(self, other):
        return self.lower_right == other.lower_right and self.upper_left == other.upper_left

    def __hash__(self):
        return hash(f'{hash(self.lower_right)}{hash(self.upper_left)}')

    def contains(self, other):
        '''
        checks if one rectangle contains the other
        :param other: other rectangle
        :return: T/F
        '''
        return self.upper_left.y > other.upper_left.y and self.upper_left.x < other.upper_left.x \
               and self.lower_right.y < other.lower_right.y and self.lower_right.x > other.lower_right.x

    def resize(self, other):
        '''
        resize the MBR to fit new rectangle
        :param other: new rectangle to be contained within MBR
        :return: resized MBR
        '''
        if self.contains(other):
            return

        if self.upper_left.x >= other.upper_left.x:
            self.upper_left.x = other.upper_left.x - 1
        if self.upper_left.y <= other.upper_left.y:
            self.upper_left.y = other.upper_left.y + 1
        if self.lower_right.y >= other.lower_right.y:
            self.lower_right.y = other.lower_right.y - 1
        if self.lower_right.x <= other.lower_right.x:
            self.lower_right.x = other.lower_right.x + 1

        self.upper_right = Coordinate(self.lower_right.x, self.upper_left.y)
        self.lower_left = Coordinate(self.upper_left.x, self.lower_right.y)

        self.area = (self.upper_right.x - self.upper_left.x) * (self.upper_left.y - self.lower_left.y)

    @classmethod
    def generate(cls, other):
        '''
        generate new MBR such that it can now contain a given rectangle
        :param other: rectangle to contain
        :return: re-sized rectangle containing r
        '''
        p = Coordinate(0, 0)
        p.x = other.upper_left.x - 1
        p.y = other.upper_left.y + 1

        q = Coordinate(0, 0)
        q.x = other.lower_right.x + 1
        q.y = other.lower_right.y - 1

        return cls(p, q)

    @classmethod
    def generate2(cls, r1, r2):
        '''
        return resize MBR such that it now contains r2 and return a copy of the original
        :param r1: rectangle to resize and copy
        :param r2: rectangle that it must contain
        :return: copy of r1 resized to fit r2
        '''
        r1_copy = cls(deepcopy(r1.upper_left), deepcopy(r1.lower_right))
        r1_copy.resize(r2)

        return r1_copy

    def euclidian_distance_rect(self, r2):
        '''
        compute euclidian distance between rectangles (based on two nearest points)
        :param r1: rectangle 1
        :param r2: rectangle 2
        :return: euclidian distance
        '''

        left = self.lower_right.x < r2.upper_left.x
        right = self.upper_left.x < r2.lower_right.x
        bottom = self.upper_left.y < r2.lower_right.y
        top = self.lower_right.y < r2.upper_left.y

        if top and left:
            return Coordinate(r2.upper_left.x, self.lower_right.y).euclidian_distance(
                                      Coordinate(self.lower_right.x, r2.upper_left.y))
        elif left and bottom:
            return Coordinate(r2.upper_left.x, r2.lower_right.y).euclidian_distance(
                                      Coordinate(self.lower_right.x, self.upper_left.y))
        elif bottom and right:
            return Coordinate(self.upper_left.x, r2.lower_right.y).euclidian_distance(
                                      Coordinate(r2.lower_right.x, self.upper_left.y))
        elif right and top:
            return Coordinate(self.upper_left.x, self.lower_right.y).euclidian_distance(
                                      Coordinate(r2.lower_right.x, r2.upper_left.y))
        elif left:
            return r2.upper_left.x - self.lower_right.x
        elif right:
            return r2.lower_right.x - self.upper_left.x
        elif bottom:
            return r2.lower_right.y - self.upper_left.y
        elif top:
            return r2.upper_left.y - self.lower_right.y
        return 0
