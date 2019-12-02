import unittest

from RTree import RTree
from Obj import Obj
from MBR import MBR
from Coordinate import Coordinate


RTreeNode = RTree.Node
POINT_OFFSET = 1


class RTreeTests(unittest.TestCase):
    def test_add_without_root_should_add_root(self):
        bounds = MBR(Coordinate(10, 10), Coordinate(20, 0))
        o = Obj('Tank', bounds)
        r_tree = RTree(4, 2)
        r_tree.insert(o)

        self.assertIsNotNone(r_tree.root)
        self.assertIsInstance(r_tree.root, RTree.Node)
        self.assertEqual(r_tree.root.mbr, MBR.generate(bounds))
        self.assertEqual(len(r_tree.root.members), 1)
        self.assertEqual(r_tree.root.members[0], o)

    def test_add_bigger_mbr_Obj_expands_root(self):
        r_tree = RTree(4, 2)
        s_Obj = Obj('SMALL_MAN', MBR(Coordinate(52, 43), Coordinate(68, 22)))
        expected_root_mbr = MBR(Coordinate(52 - POINT_OFFSET, 43 + POINT_OFFSET), Coordinate(68 + POINT_OFFSET, 22 - POINT_OFFSET))
        r_tree.insert(s_Obj)
        self.assertEqual(r_tree.root.mbr, expected_root_mbr)

        # Add a bigger Obj
        expected_root_mbr = MBR(Coordinate(20 - POINT_OFFSET, 45 + POINT_OFFSET), Coordinate(70 + POINT_OFFSET, 20 - POINT_OFFSET))
        b_Obj = Obj('BIG_MAN', MBR(Coordinate(20, 45), Coordinate(70, 20)))
        r_tree.insert(b_Obj)

        self.assertEqual(r_tree.root.mbr, expected_root_mbr)
        self.assertCountEqual(r_tree.root.members, [b_Obj, s_Obj])


    """
    The split_leaf function should split a leaf full of entries into two separate nodes.
    It should pick the two furthest apart entries and make their MBRs into nodes.
        Then, from the left-over entries, it should choose to insert them into the node which requires least expansion
    """
    def test_split(self):
        """
        -----------------------------------------------------------------------------------------------------
        |                                                      |------------------------------------------| |
        |                                                      |                                          | |
        |                                         ______       |                                          | |
        |     ______________                      |     |      |                                          | |
        |    |             |                      |     |      |                                          | |
        |    |     A       |                      |     |      |                                          | |
        |    |             |                      |     |      |                                          | |
        |    |     ________|________              |     |      |                                          | |
        |    |     |       |       |              |  C  |      |                  D                       | |
        |    |     |       |       |              |     |      |                                          | |
        |    |     |       |       |              |     |      |                                          | |
        |    |     |       |B      |              |     |      |                                          | |
        |    --------------        |              |     |      |                                          | |
        |          |               |              |     |      |                                          | |
        |          |               |              |     |      |                                          | |
        |          -----------------              |     |      |                                          | |
        |                                         -------      |                                          | |
        |                                                      |                                          | |
        |                                                      |__________________________________________| |
        |                                                                                                   |
        _____________________________________________________________________________________________________
        Here, A and D should be chosen as the basis for the two new nodes.
            B should go to the A node and C should go to the D node, as that would require the least expansion from both sides
        -----------------------------------------------------------------------------------------------------
        |                                        _____________________________Node B________________________|
        |                                        |             |------------------------------------------|||
        |                                        |             |                                          |||
        |  ______Node A______________            |______       |                                          |||
        |  |  ______________        |            ||     |      |                                          |||
        |  | |             |        |            ||     |      |                                          |||
        |  | |     A       |        |            ||     |      |                                          |||
        |  | |             |        |            ||     |      |                                          |||
        |  | |     ________|________|            ||     |      |                                          |||
        |  | |     |       |       ||            ||  C  |      |                  D                       |||
        |  | |     |       |       ||            ||     |      |                                          |||
        |  | |     |       |       ||            ||     |      |                                          |||
        |  | |     |       |B      ||            ||     |      |                                          |||
        |  | --------------        ||            ||     |      |                                          |||
        |  |       |               ||            ||     |      |                                          |||
        |  |       |               ||            ||     |      |                                          |||
        |  |       -----------------|            ||     |      |                                          |||
        |  |------------------------|            |-------      |                                          |||
        |                                        |             |                                          |||
        |                                        |             |__________________________________________|||
        |                                         --------------------------------------------------------- |
        ____________________________________________________________________________________________________|
       Both nodes should be 1 Coordinate bigger than the nodes
        """
        root = RTree.Node(MBR(Coordinate(20, 45), Coordinate(70, 20)), 4, 2)
        Obj_a = Obj('A', MBR(Coordinate(22, 40), Coordinate(30, 30)))
        Obj_b = Obj('B', MBR(Coordinate(25, 35), Coordinate(40, 25)))
        Obj_c = Obj('C', MBR(Coordinate(44, 40), Coordinate(47, 25)))
        Obj_d = Obj('D', MBR(Coordinate(52, 43), Coordinate(68, 22)))
        root.members = [Obj_a, Obj_b, Obj_c, Obj_d]

        expected_node_a_mbr = MBR(Coordinate(22 - POINT_OFFSET, 40 + POINT_OFFSET),
                                        Coordinate(40 + POINT_OFFSET, 25 - POINT_OFFSET))
        expected_node_b_mbr = MBR(Coordinate(44 - POINT_OFFSET, 43 + POINT_OFFSET),
                                        Coordinate(68 + POINT_OFFSET, 22 - POINT_OFFSET))

        node_a, node_b = root.split()

        self.assertEqual(node_a.mbr, expected_node_a_mbr)
        self.assertEqual(node_b.mbr, expected_node_b_mbr)
        self.assertCountEqual(node_a.members, [Obj_a, Obj_b])
        self.assertCountEqual(node_b.members, [Obj_c, Obj_d])
        self.assertEqual(node_a.children, [])
        self.assertEqual(node_b.children, [])

    def test_find_min_expansion_node(self):
        """
        Given 3 nodes and one Obj, find the node which requires the minimum expansion to accommodate the Obj
        """
        """
        Node C should be chosen
        -----------------------------------------------------------------------------------------------------
        |                                                      |------------------------------------------| |
        |                                                      |                                          | |
        |                                         ______       |                                          | |
        |     ______________                      |     |      |                                          | |
        |    |             |                      |     | ---  |                                          | |
        |    |     A       |                      |     | |  | |                                          | |
        |    |             |                      |     | |E | |                                          | |
        |    |     ________|________              |     | |  | |                                          | |
        |    |     |       |       |              |  C  |  --  |                  D                       | |
        |    |     |       |       |              |     |      |                                          | |
        |    |     |       |       |              |     |      |                                          | |
        |    |     |       |B      |              |     |      |                                          | |
        |    --------------        |              |     |      |                                          | |
        |          |               |              |     |      |                                          | |
        |          |               |              |     |      |                                          | |
        |          -----------------              |     |      |                                          | |
        |                                         -------      |                                          | |
        |                                                      |                                          | |
        |                                                      |__________________________________________| |
        |                                                                                                   |
        _____________________________________________________________________________________________________
        """
        rtn_a = RTree.Node(MBR(Coordinate(22, 40), Coordinate(30, 30)), 4, 2)
        rtn_b = RTree.Node(MBR(Coordinate(25, 35), Coordinate(40, 25)), 4, 2)
        rtn_c = RTree.Node(MBR(Coordinate(44, 40), Coordinate(47, 25)), 4, 2)
        rtn_d = RTree.Node(MBR(Coordinate(52, 43), Coordinate(68, 22)), 4, 2)
        Obj_e = Obj('E', MBR(Coordinate(47, 35), Coordinate(51, 30)))

        min_expansion_node = RTree.Node.find_min([rtn_a, rtn_b, rtn_c, rtn_d], Obj_e)
        self.assertEqual(rtn_c, min_expansion_node)

    def test_find_min_expansion_node_chooses_node_that_contains_it_already(self):
        """
        Should choose D
        -----------------------------------------------------------------------------------------------------
        |                                                      |------------------------------------------| |
        |                                                      |                                          | |
        |                                         ______       |                                          | |
        |     ______________                      |     |      |              ------                      | |
        |    |             |                      |     |      |             |  E  |                      | |
        |    |     A       |                      |     |      |             ------                       | |
        |    |             |                      |     |      |                                          | |
        |    |     ________|________              |     |      |                                          | |
        |    |     |       |       |              |  C  |      |                  D                       | |
        |    |     |       |       |              |     |      |                                          | |
        |    |     |       |       |              |     |      |                                          | |
        |    |     |       |B      |              |     |      |                                          | |
        |    --------------        |              |     |      |                                          | |
        |          |               |              |     |      |                                          | |
        |          |               |              |     |      |                                          | |
        |          -----------------              |     |      |                                          | |
        |                                         -------      |                                          | |
        |                                                      |                                          | |
        |                                                      |__________________________________________| |
        |                                                                                                   |
        _____________________________________________________________________________________________________
        """
        rtn_a = RTree.Node(MBR(Coordinate(22, 40), Coordinate(30, 30)), 4, 2)
        rtn_b = RTree.Node(MBR(Coordinate(25, 35), Coordinate(40, 25)), 4, 2)
        rtn_c = RTree.Node(MBR(Coordinate(44, 40), Coordinate(47, 25)), 4, 2)
        rtn_d = RTree.Node(MBR(Coordinate(52, 43), Coordinate(68, 22)), 4, 2)
        Obj_e = Obj('E', MBR(Coordinate(55, 35), Coordinate(60, 30)))

        min_expansion_node = RTree.Node.find_min([rtn_a, rtn_b, rtn_c, rtn_d], Obj_e)
        self.assertEqual(min_expansion_node, rtn_d)


if __name__ == '__main__':
    unittest.main()