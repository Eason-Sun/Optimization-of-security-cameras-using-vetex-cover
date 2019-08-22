import unittest
from streetGraphGen import Point
from streetGraphGen import Line
from streetGraphGen import Street
from streetGraphGen import Graph
from streetGraphGen import inputParser


class TestStreet(unittest.TestCase):

    def setUp(self):
        self.street = Street()

    def test_addStreet(self):
        self.street = Street()
        self.street.addStreet("King St", [(0, 0), (1, 1), (2, 2)])
        self.street.addStreet("Queen St", [(0, 2), (1, 1), (2, 0)])
        expectedStreets = {"King St": [Point((0, 0)), Point((1, 1)), Point((2, 2))],
                           "Queen St": [Point((0, 2)), Point((1, 1)), Point((2, 0))]}
        self.assertEqual(self.street.streets, expectedStreets)

    def test_changeStreet(self):
        self.street = Street()
        self.street.addStreet("King St", [(0, 0), (1, 1), (2, 2)])
        self.street.addStreet("Queen St", [(0, 2), (1, 1), (2, 0)])
        self.street.changeStreet("King St", [(-1, -1), (1, 1), (2, 2)])
        expectedStreets = {"King St": [Point((-1, -1)), Point((1, 1)), Point((2, 2))],
                           "Queen St": [Point((0, 2)), Point((1, 1)), Point((2, 0))]}
        self.assertEqual(self.street.streets, expectedStreets)

    def test_removeStreet(self):
        self.street = Street()
        self.street.addStreet("King St", [(0, 0), (1, 1), (2, 2)])
        self.street.addStreet("Queen St", [(0, 2), (1, 1), (2, 0)])
        self.street.removeStreet("Queen St")
        expectedStreets = {"King St": [Point((0, 0)), Point((1, 1)), Point((2, 2))]}
        self.assertEqual(self.street.streets, expectedStreets)

    def test_findStreetSegments(self):
        self.street = Street()
        self.street.addStreet("King St", [(0, 0), (1, 1), (2, 2)])
        self.street.addStreet("Queen St", [(0, 2), (1, 1), (2, 0)])
        streetsSegments = self.street.findStreetSegments()
        expectedStreetsSegments = [[Line(Point((0, 0)), Point((1, 1))), Line(Point((1, 1)), Point((2, 2)))],
                                   [Line(Point((0, 2)), Point((1, 1))), Line(Point((1, 1)), Point((2, 0)))]]
        self.assertEqual(streetsSegments, expectedStreetsSegments)

    def test_findCoefficients(self):
        self.street = Street()
        line = Line(Point((0, 1)), Point((2, 3)))
        expectedA = 2
        expectedB = -2
        expectedC = -2
        self.assertEqual((expectedA, expectedB, expectedC), self.street.findCoefficients(line))

    def test_isOverlap(self):
        line1 = Line(Point((1, 1)), Point((4, 4)))
        line2 = Line(Point((2, 2)), Point((3, 3)))
        line3 = Line(Point((1, 2)), Point((2, 1)))
        self.assertTrue(self.street.isOverlap(line1, line2))
        self.assertFalse(self.street.isOverlap(line1, line3))
        self.assertFalse(self.street.isOverlap(line3, line2))

    def test_is_between(self):
        point1 = Point((1, 1))
        point2 = Point((2, 2))
        point3 = Point((3, 3))
        point4 = Point((5, 6))
        self.assertTrue(self.street.is_between(point2, point1, point3))
        self.assertFalse(self.street.is_between(point4, point1, point3))

    def test_findLineIntersection(self):
        line1 = Line(Point((1, 1)), Point((3, 3)))
        line2 = Line(Point((1, 3)), Point((3, 1)))
        expectedIntersect = Point((2, 2))
        self.assertEqual(expectedIntersect, self.street.findLineIntersection(line1, line2))

    def test_findStreetIntersections(self):
        self.street.addStreet("Weber Street", [(2, -1), (2, 2), (5, 5), (5, 6), (3, 8)])
        self.street.addStreet("King Street South", [(4, 2), (4, 8)])
        self.street.addStreet("Davenport Road", [(1, 4), (5, 8)])
        self.street.findStreetIntersections()
        s1 = set()
        s1.update([Line(Point((5, 6)), Point((3, 8))), Line(Point((1, 4)), Point((5, 8))),
                   Line(Point((4, 2)), Point((4, 8)))])
        s2 = set()
        s2.update([Line(Point((2, 2)), Point((5, 5))), Line(Point((4, 2)), Point((4, 8)))])
        expectedIntersectLineDict = {Point((4, 7)): s1, Point((4, 4)): s2}
        self.assertEqual(expectedIntersectLineDict, self.street.intersectLineDict)
        s3 = set()
        s3.update([Point((4, 4)), Point((4, 7))])
        exptectedLineWithMultiIntersectDict = {Line(Point((4, 2)), Point((4, 8))): s3}
        self.assertEqual(exptectedLineWithMultiIntersectDict, self.street.lineWithMultiIntersectDict)
        expectedSingleIntersectLines = {Line(Point((5, 6)), Point((3, 8))): Point((4, 7)),
                                        Line(Point((1, 4)), Point((5, 8))): Point((4, 7)),
                                        Line(Point((2, 2)), Point((5, 5))): Point((4, 4))}
        self.assertEqual(expectedSingleIntersectLines, self.street.singleIntersectLines)


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.street = Street()
        self.graph = Graph(self.street)
        self.street.addStreet("Weber Street", [(2, -1), (2, 2), (5, 5), (5, 6), (3, 8)])
        self.street.addStreet("King Street South", [(4, 2), (4, 8)])
        self.street.addStreet("Davenport Road", [(1, 4), (5, 8)])

    def test_graphGen(self):
        self.graph.graphGen()
        realGraph = self.graph.graph
        expectedGraph = {Point((4, 4)): [Point((2, 2)), Point((4, 2)), Point((5, 5)), Point((4, 7))],
                         Point((4, 7)): [Point((3, 8)), Point((4, 8)), Point((5, 8)), Point((5, 6)), Point((4, 4)),
                                         Point((1, 4))]}
        for intersection in realGraph:
            self.assertTrue(intersection in expectedGraph)
            self.assertEqual(len(realGraph[intersection]), len(expectedGraph[intersection]))
            self.assertEqual(set(realGraph[intersection]), set(expectedGraph[intersection]))

    def test_rmDuplicates(self):
        self.graph.graphGen()
        self.graph.rmDuplicates()
        realGraph = self.graph.graph
        expectedGraph = {Point((4, 4)): [Point((2, 2)), Point((4, 2)), Point((5, 5)), Point((4, 7))],
                         Point((4, 7)): [Point((3, 8)), Point((4, 8)), Point((5, 8)), Point((5, 6)), Point((1, 4))]}
        for intersection in realGraph:
            self.assertTrue(intersection in expectedGraph)
            self.assertEqual(len(realGraph[intersection]), len(expectedGraph[intersection]))
            self.assertEqual(set(realGraph[intersection]), set(expectedGraph[intersection]))


class TestParser(unittest.TestCase):

    def setUp(self):
        self.street = Street()
        self.street.addStreet("King Street South", [(4, 2), (4, 8)])

    def test_inputParser(self):
        self.assertEqual(inputParser("\n", self.street), ["p"])
        self.assertEqual(inputParser("g", self.street), ["g"])
        self.assertEqual(inputParser("r \"Queen St\"", self.street), ["Error: ", "The street does not exist."])
        self.assertEqual(inputParser("r \"King Street South\"", self.street), ["r", "King Street South"])
        self.assertEqual(inputParser("r \"\"", self.street), ["Error: ", "Invalid street name in your command."])
        self.assertEqual(inputParser("r King Street South", self.street), ["Error: ", "Lack of quotation mark for the street name."])
        self.assertEqual(inputParser("a \"King Street South\" (4, 2) (4, 8)", self.street), ["Error: ", "This street has already been added."])
        self.assertEqual(
            inputParser("a \"Weber Street\"      ( 2,-1 )    (2 , 2)  ( 5, 5)     (5 ,6 )  ( 3 , 8 )", self.street),
            ["a", "Weber Street", "      ( 2,-1 )    (2 , 2)  ( 5, 5)     (5 ,6 )  ( 3 , 8 )"])
        self.assertEqual(inputParser("c \"Queen St\" (3, 1) (4, 8)", self.street),
                         ["Error: ", "The street does not exist."])
        self.assertEqual(inputParser("c \"King Street South\"    (2   ,1 ) (  2,   2    )", self.street),
                         ["c", "King Street South", "    (2   ,1 ) (  2,   2    )"])
        self.assertEqual(inputParser("ewrfda", self.street),
                         ["Error: ", "'a' or 'c' or 'r' specified for a street that does not exist."])


if __name__ == '__main__':
    unittest.main()
