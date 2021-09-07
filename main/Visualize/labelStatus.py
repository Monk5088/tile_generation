import sys
sys.path.insert(0,'..')

from Classes.polygon import Polygon
from Classes.rectangle import Rectangle
from Classes.ellipse import Ellipse
from Classes.tile import Tile

def makeAnnotations(filename):
    """
        Generates polygons/ellipses (whichever applicable) for all annotations

        Args:
            filename: name of file outputted by parseXML.py

        Returns:
            An array of all annotations
    """
    annotations = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.split()
            type_name = line[0]
            label = line[1]
            if (type_name == "1"):            
                p1 = (float(line[2]), float(line[3]))
                p2 = (float(line[4]), float(line[5]))
                p3 = (float(line[6]), float(line[7]))
                p4 = (float(line[8]), float(line[9]))
                vertices = [p1, p2, p3, p4, p1]
                annotation = Rectangle(vertices, label) 
                annotations.append(annotation)
            elif (type_name == "2"):
                x1 = float(line[2])
                y1 = float(line[3])
                x2 = float(line[4])
                y2 = float(line[5])
                annotation = Ellipse(x1, y1, x2, y2, label)
                annotations.append(annotation)
            else:
                i = 2
                vertices = []
                while (i < len(line)):
                    vertex = (float(line[i]), float(line[i+1]))
                    vertices.append(vertex)
                    i += 2
                annotation = Polygon(vertices, label)
                annotations.append(annotation)
        return annotations

def updateStatus(tiles, poly):
    """
        Updates the status of all the given tiles wrt the given annotation (poly)

        Args:
            tiles: 2-D array of tiles of ROI
            poly: polygon/ellipse object corresponding to the annotation in question
            filename: name of the output file
    """
    for i in range(len(tiles)):
        for j in range(len(tiles[0])):
            try:
                tiles[i][j].updateLabelStatus(poly)
            except Exception as e: 
                pass

