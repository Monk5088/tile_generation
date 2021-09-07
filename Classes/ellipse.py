import shapely
import math

class Ellipse(object):
    def __init__(self, x1, y1, x2, y2, label = ""):
        """
        Constructor for ellipse class

        Args:
            top left corner (x1, y1) and bottom right corner (x2, y2) of the bounding box of the ellipse.
            label is optional
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2 
        self.label = label
        self.centre = (float(self.x1+self.x2)/2, float(self.y1+self.y2)/2)
        self.a = abs(float(self.x2-self.x1)/2)
        self.b = abs(float(self.y2-self.y1)/2)
        circle = shapely.geometry.Point(self.centre).buffer(1)
        self.polygon = shapely.affinity.scale(circle, self.a, self.b)

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def setVertices(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2 
        self.centre = (float(self.x1+self.x2)/2, float(self.y1+self.y2)/2)
        self.a = abs(float(self.x2-self.x1)/2)
        self.b = abs(float(self.y2-self.y1)/2)
        circle = shapely.geometry.Point(self.centre).buffer(1)
        self.polygon = shapely.affinity.scale(circle, self.a, self.b)

    def getDetails(self):
        return [self.centre, self.a, self.b]

    def getArea(self):
        return (math.pi)*(self.a)*(self.b)

    def isIntersecting(self, poly):
        """
        Checks whether the given ellipse intersects with a polygon

        Args:
            The other polygon that is to be checked for intersection

        Returns:
            A boolean result true/false
        """
        return (self.polygon).intersects(poly.polygon)

    def contained(self, poly):
        """
        Checks whether the given ellipse contains the given polygon

        Args:
            The other polygon that is to be checked for containment

        Returns:
            A boolean result true/false
        """
        return (self.polygon).contains(poly.polygon)

    def getBounds(self):
        min_x = min([self.x1,self.x2])
        max_x = max([self.x1,self.x2])
        min_y = min([self.y1,self.y2])
        max_y = max([self.y1,self.y2])
        return (min_x, min_y, max_x, max_y)
        
    def pointLocation(self, x, y):
        value = (float((x-self.centre[0])**2)/(self.a)**2) + (float((y-self.centre[1])**2)/(self.b)**2)
        if (value == 1):
            return 1 # Boundary
        elif (value < 1):
            return 0 # Inside
        else:
            return 2 # Outside

    
    


    