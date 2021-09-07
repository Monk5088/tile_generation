import sys
sys.path.append("C:\Digital_Histopathology\Tile_generation")

from Classes.polygon import Polygon
from Classes.rectangle import Rectangle
from Classes.tile import Tile
import math


def getROI(x1, y1, x2, y2):
    """
        Creates a rectangle object for the region of interest
    
        Args:
            x1, y1: top left corner of ROI
            x2, y2: bottom right corner of ROI
    
        Returns:
            Object of Rectangle class for the ROI
    """
    p1 = (x1, y1)
    p2 = (x2, y1)
    p3 = (x2, y2)
    p4 = (x1, y2)
    vertices = [p1, p2, p3, p4, p1]
    roi = Rectangle(vertices)
    return roi

def getTiles(roi, tilesize):
    """
        Creates a tile object of the specified size spanning the region of interest

        Args:
            roi: rectangle object of roi
            tilesize: size of tiles to be generated

        Returns:
            A 2-D array of tile objects
    """
    xmin, ymin, xmax, ymax = roi.getBounds()
    x = (math.floor(xmin/tilesize))
    y = (math.floor(ymin/tilesize))
    X = (math.ceil(xmax/tilesize))
    Y = (math.ceil(ymax/tilesize))
    tiles = []
    for i in range(x, X):
        row = []
        for j in range(y, Y):
            row.append(Tile(tilesize, i*tilesize, j*tilesize))
        tiles.append(row)

    return tiles

