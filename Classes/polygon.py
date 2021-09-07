from shapely.geometry import Polygon as SPoly
from shapely.geometry import Point as SPoint

class Polygon(object):
    def __init__(self, vertices, label=""):
        """
        Constructor for polygon class

        Args:
            Array of tuples, each tuple contains an x-y pair denoting a vertex of the polygon
            label is optional
        """
        self.label = label
        self.vertices = vertices
        self.polygon = SPoly(vertices)

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def getArea(self):
        return (self.polygon).area

    def setVertices(self, vertices):
        self.vertices = vertices
        self.polygon = SPoly(vertices)

    def getVertices(self):
        return self.vertices

    def isIntersecting(self, poly):
        """
        Checks whether the given polygon intersects with another polygon

        Args:
            The other polygon that is to be checked for intersection

        Returns:
            A boolean result true/false
        """
        return (self.polygon).intersects(poly.polygon)

    def contained(self, poly):
        """
        Checks whether the given polygon contains the given polygon

        Args:
            The other polygon that is to be checked for containment

        Returns:
            A boolean result true/false
        """
        return (self.polygon).contains(poly.polygon)

    def getBounds(self):
        return (self.polygon).bounds

    def pointLocation(self, x, y):
        point = SPoint(x, y)
        if ((self.polygon).touches(point)):
            return 1 # Boundary
        elif ((self.polygon).contains(point)):
            return 0 # Inside
        else:
            return 2 # Outside