class Obj:
    '''
    Object to be stored in RTree
    '''
    def __init__(self, val, mbr):
        self.val = val
        self.mbr = mbr

    def __eq__(self, other):
        return self.val == other.val and self.mbr == other.mbr

    def __hash__(self):
        return hash(f'{self.val}{hash(self.mbr)}')