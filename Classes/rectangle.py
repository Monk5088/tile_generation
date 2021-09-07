import shapely
from Classes.polygon import Polygon

class Rectangle(Polygon):
    def __init__(self, vertices, label = ""):
        """
        Constructor for rectangle class. This class inherits from polygon

        Args:
            Array of tuples, each tuple contains an x-y pair denoting a vertex of the polygon
            label is optional
        """
        self.x1 = vertices[0][0]
        self.x2 = vertices[1][0]
        self.y1 = vertices[0][1]
        self.y2 = vertices[2][1]
        Polygon.__init__(self, vertices, label)

    def getArea(self):
        length = abs(self.x1 - self.x2)
        width = abs(self.y1 - self.y2)
        return length*width

    def getBounds(self):
        min_x = min([self.x1,self.x2])
        max_x = max([self.x1,self.x2])
        min_y = min([self.y1,self.y2])
        max_y = max([self.y1,self.y2])
        return (min_x, min_y, max_x, max_y)

    def pointLocation(self, x, y):
        if((x == self.x1 and self.y1 <= y <= self.y2) or (x == self.x2 and self.y1 <= y <= self.y2) or (y == self.y1 and self.x1 <= x <= self.x2) or (y == self.y2 and self.x1 <= x <= self.x2)):
            return 1 # Boundary
        elif(self.x1 < x < self.x2 and self.y1 < y < self.y2): # Inside
            return 0 # Inside
        return -1 # Outside


    
        

