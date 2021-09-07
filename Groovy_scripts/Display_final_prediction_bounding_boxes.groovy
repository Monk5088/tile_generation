import qupath.lib.roi.ROIs
import qupath.lib.roi.RoiTools
import qupath.lib.objects.PathObjects
import qupath.lib.regions.ImagePlane
import qupath.lib.scripting.QP
import qupath.lib.geom.Point2
import qupath.lib.roi.PolygonROI
import qupath.lib.objects.PathAnnotationObject
import qupath.lib.images.servers.ImageServer

def hierarchy = QP.getCurrentHierarchy()
def rotated = true

//Change the path of the file here
//path = "C:\\Users\\Lenovo\\Downloads\\mitosis_regions_intersected_xml (3).xml"
def server = QP.getCurrentImageData().getServer()
def h = server.getHeight()
def w = server.getWidth()
path ="C:\\Users\\user\\Downloads\\mitosis_regions_intersected_xml (1).xml"
def file = new File(path)
def text = file.getText()

def list = new XmlSlurper().parseText(text)
print(list)
list.Annotation.each {
    def annotationClass = getPathClass(it.@Name.toString())
    def annotationColor = getPathClass(it.@LineColor.toString())
    it.Regions.Region.each { region ->
        def tmp_points_list = []
        region.Vertices.Vertex.each{ vertex ->
            if (rotated) {
                X = vertex.@X.toDouble()
                Y = vertex.@Y.toDouble()
            }
            else {
                X = vertex.@Y.toDouble()
                Y = h - vertex.@X.toDouble()
                
            }
            tmp_points_list.add(new Point2(X, Y))
        }
        def roi1 = new PolygonROI(tmp_points_list)
        def annotation = new PathAnnotationObject(roi1)
        annotation.setPathClass(annotationClass)
        
        if(String.valueOf(annotationColor)=='65280'){
          annotation.setColorRGB(getColorRGB(0,255,0)) //Green  - Prediction True 
        }
        
        else if(String.valueOf(annotationColor)=='16776960'){
             annotation.setColorRGB(getColorRGB(255,0,0))//True Negative 
        }
        
        else if(String.valueOf(annotationColor)=='65535'){
            annotation.setColorRGB(getColorRGB(0,0,255))//Blue - False Positive
        }
        
        else if(String.valueOf(annotationColor)=='255'){
            annotation.setColorRGB(getColorRGB(255,0,0))//Red - Prediction false
        }
               
        else if(String.valueOf(annotationColor)=='4194368'){
             annotation.setColorRGB(getColorRGB(0,0,0))//Black - False Negative
       }
       
       else if(String.valueOf(annotationColor)=='16744448'){
             annotation.setColorRGB(getColorRGB(0,255,0)) //Green - True Positive
       }
       
        hierarchy.addPathObject(annotation, false)
    }
}

fireHierarchyUpdate()


Dialogs.showPlainMessage("Color Notation",
"""
True Positive:  Greeen
True Negative: Red
False Positive: Blue
False Negative: Black

""")

print "Done!"



