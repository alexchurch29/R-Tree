from PIL import Image, ImageDraw, ImageFont
from random import randint

class Drawer:
    '''
    draw rtree
    :param rtree: rtree to draw
    :return:
    '''

    def __init__(self, rtree=None):
        self.rtree = rtree
        self.canvas = Image.new('RGB', (1000, 600), (256, 256, 256))
        self.drawer = ImageDraw.Draw(self.canvas, 'RGBA')

    def draw(self):
        root = self.rtree.root
        nodes = list()
        nodes.append(root)
        while nodes[0].depth != 1:
            n = nodes.pop(0)
            if n.depth > 1:
                for i in n.children:
                    nodes.append(i)
            r, g, b = randint(0, 256), randint(0, 256), randint(0, 256)
            self.drawer.rectangle(
                (n.mbr.lower_left.x * 10, n.mbr.lower_left.y * 10,
                 n.mbr.upper_right.x * 10, n.mbr.upper_right.y * 10),
                fill=(r, g, b, 50),
                outline=(0, 0, 0, 256))
        while len(nodes) > 0:
            n = nodes.pop(0)
            r, g, b = randint(0, 256), randint(0, 256), randint(0, 256)
            self.drawer.rectangle(
                (n.mbr.lower_left.x * 10, n.mbr.lower_left.y * 10,
                 n.mbr.upper_right.x * 10, n.mbr.upper_right.y * 10),
                fill=(r, g, b, 50),
                outline=(0, 0, 0, 256))
            for i in n.children:
                self.drawer.rectangle((i.mbr.lower_left.x*10, i.mbr.lower_left.y*10, i.mbr.upper_right.x*10, i.mbr.upper_right.y*10),
                                      fill=(r, g, b, 50),
                                      outline=(0, 0, 0, 256))
                self.drawer.text((i.mbr.upper_left.x * 10, i.mbr.upper_left.y * 10),
                                 i.val, fill=(255,255,255,255))
        self.canvas.show()
