from math import sqrt


class Coordinate:
    '''
    Defines a coordinate on the x, y plane
    '''
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        if self.euclidian_distance(other) == 0:
            return True
        return False

    def __hash__(self):
        return hash(f'{self.x}{self.y}')

    def euclidian_distance(self, other):
        '''
        compute euclidian euclidian_distanceance between Coordinates
        :param p1: point 1
        :param p2: point 2
        :return: euclidian euclidian_distanceance
        '''
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
