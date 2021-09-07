#import sys
from Classes.polygon import Polygon
# Considering origin to be top left
class Tile(Polygon):
    def __init__(self, size, x, y, label=""):
        """
        Constructor for tile class. This class inherits from polygon
        Args:
            size: tiles side length
            x, y: top left corner of the tile
            label is optional
        """
        self.size = size
        # Top left corner
        self.x1 = x
        self.y1 = y
        # Bottom right corner
        self.x2 = self.x1 + self.size
        self.y2 = self.y1 + self.size
        self.labelStatus = {}
        vertices = [(self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2), (self.x1, self.y2), (self.x1, self.y1)]
        Polygon.__init__(self, vertices, label)
    def setSize(self, size):
        self.size = size
    def getSize(self):
        return self.size
    def setVertices(self, x, y):
        # Top left corner
        self.x1 = x
        self.y1 = y
        # Bottom right corner
        self.x2 = self.x1 + self.size
        self.y2 = self.y1 + self.size
        vertices = [(self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2), (self.x1, self.y2), (self.x1, self.y1)]
        Polygon.setVertices(self, vertices)
    def updateLabelStatus(self, poly):
        """
        Updates the status of a tile wrt an annotation (represented by poly)
        Different types of status:
            Tile is completely inside poly - 0
            Tile intersects the boundary of poly - 1
            Tile is completely outside poly - 2
            Poly lies completely inside the tile - 3
        Args:
            poly: the polygon that denotes an annotation
        Returns:
            void
            This function doesn't return anything but it updates the status of the tile with respect to
            various annotations with the help of a dictionary. It also stores the percentage of overlap
            of the tile with poly
        """
        
        label = poly.label
        p1 = poly.polygon.buffer(0)
        p2 = self.polygon.buffer(0)
        #print(poly.polygon)
        #print(self.polygon)
        #print(label)
        isInsideTile = (self).contained(poly)
        isIntersection = poly.isIntersecting(self)
        isContained = poly.contained(self)
        if (isInsideTile):
            #intersection_area = ((poly.polygon).intersection(self.polygon)).area
            intersection_area = ((p1).intersection(p2)).area
            percent_overlap = (float(intersection_area)/self.getArea())*100
            self.labelStatus[label] = [3,percent_overlap] # polygon lies inside tile self.labelStatus[label] = (3, percent_overlap)
        elif (isContained):
            self.labelStatus[label] = [0,100] # tile lies completely inside the boundary of the polygon self.labelStatus[label] = (3, 100) 
        elif (isIntersection):
            #intersection_area = ((poly.polygon).intersection(self.polygon)).area
            intersection_area = ((p1).intersection(p2)).area
            percent_overlap = (float(intersection_area)/self.getArea())*100
            self.labelStatus[label] = [1,percent_overlap] # tile intersects the boundary of the polygon self.labelStatus[label] = (3, percent_overlap)
    
    def getLabelStatus(self):
        return self.labelStatus