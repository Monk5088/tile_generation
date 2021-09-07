import xml.etree.ElementTree as ET

from shapely.geometry import Polygon as SPoly
from shapely.geometry import Point as SPoint

def parseXML(xmlfile, roi_coords,output_path):
    """
        Reading the coodinates of the annotations from an XML file

        Args:
            The file path of the XML file from which the values are read
            The coordinates for the ROI (Region of Interest)

        Returns:
            string
            The file path of the destination file containg the coordinates of the annotations
            A quadtree which consists of all the labelled annotations

    """
  
    x1 =roi_coords[0]
    y1 =roi_coords[1]
    x2 =roi_coords[2]
    y2=roi_coords[3]

    vertices=[(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
    polygon = SPoly(vertices)
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    ver = []
    v=[]
    labels = []
    for region in root.findall("./Annotation/Regions/Region"):
        temp = []
        label = "".join([region.get("Text").replace(" ", ""),region.get("Id")])
        if(region.get("Text")!=""):
            temp.append(region.get("Type"))
            temp.append(label)
            for vertex in region.findall("./Vertices/Vertex"):
                x = vertex.get("X")
                y = vertex.get("Y")
                temp.append([x,y])
                ver.append([int(float(x)),int(float(y))])
            try:
                #poly = SPoly(ver)
                #if((polygon).contains(poly) or (polygon).intersects(poly) ): 
                labels.append(label)
                v.append(temp)
                ver=[]
            except Exception as e:
                pass
    dest = "".join([str(output_path[0:-6]),"\\",str(roi_coords[0]),"_",str(roi_coords[1]),"_",str(roi_coords[2]),"_",str(roi_coords[3]),".txt"])
    with open(dest,"w") as f:
        for i in range(len(v)):
            f.write("".join([str(v[i][0])," "]))
            f.write("".join([str(v[i][1])," "]))
            for j in range(2,len(v[i])):
                f.write("".join([str(v[i][j][0])," ",str(v[i][j][1])," "]))
            f.write("\n")
    with open("C:/Digital_Histopathology/Tile_generation/inputfile.txt","a") as file:
        for i in labels:
            file.write(i)
            file.write("\n")
    return dest,labels
