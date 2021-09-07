import qupath.lib.roi.ROIs
import qupath.lib.roi.RoiTools
import qupath.lib.objects.PathObjects
import qupath.lib.regions.ImagePlane
import qupath.lib.scripting.QP
import qupath.lib.geom.Point2
import qupath.lib.roi.PolygonROI
import qupath.lib.objects.PathAnnotationObject
import qupath.lib.images.servers.ImageServer

def plane = ImagePlane.getDefaultPlane()
//Aperio Image Scope displays images in a different orientation
def rotated = true // if rotated=true you have to rotate the WSI to 90 degrees. View-> Rotate->90 degrees
def server = QP.getCurrentImageData().getServer()
def h = server.getHeight()
def w = server.getWidth()
// need to add annotations to hierarchy so qupath sees them
def hierarchy = QP.getCurrentHierarchy()
//Prompt user for exported aperio image scope annotation file
def path = server.getURIs().getAt(0).getPath();           // HERE
path = path.substring(0, path.lastIndexOf(".")) + ".xml"  // HERE

def file = new File(path)
def text = file.getText()
def list = new XmlSlurper().parseText(text)
c= 0
List<String> careerNavbarList = new ArrayList<>()
list.Annotation.each {
    // Get the class from your XML
    def annotationClass = getPathClass(it.@Name.toString())
    //print(annotationClass)
    def annotationColor = getPathClass(it.@LineColor.toString())

    it.Regions.Region.each { region ->
        c = 0
        def tmp_points_list = []
        ell = region.@Type.toString()
        textname =region.@Id.toString()
        textId = region.@Text.toString()
        xnames =[]
        region.Vertices.Vertex.each{ vertex ->
            if (rotated) {
                X = vertex.@X.toDouble()
                Y = vertex.@Y.toDouble()
                if(String.valueOf(ell)=='2'){
                  if(c==1){
                    def u1 = X
                    def u2 = Y
                    v1 = Double.parseDouble(careerNavbarList[0])
                    v2 = Double.parseDouble(careerNavbarList[1])
                    widthh = Math.abs(v1-u1)
                    heightt = Math.abs(v2-u2)
                    def roi2 =ROIs.createEllipseROI(v1,v2,widthh,heightt,plane)
                    d1 = roi2.getShape()
                    def annotation1 = PathObjects.createAnnotationObject(roi2)
                    annotation1.setColorRGB(getColorRGB(0,102,0))
                    //annotation1.name= textId.concat(textname)             
                    addObject(annotation1)                                         
                  }
                if(c==0){
                    def v1 = X
                    def v2 = Y
                    careerNavbarList.add(v1.toString())
                    careerNavbarList.add(v2.toString())
                    c =c+1
                }
               }
            tmp_points_list.add(new Point2(X, Y))         
            }
            else {
                X = vertex.@Y.toDouble()
                Y = h - vertex.@X.toDouble()
                
                if(String.valueOf(ell)=='2'){
                if(c==1){
                    def u1 = X
                    def u2 = Y
                    v1 = Double.parseDouble(careerNavbarList[0])
                    v2 = Double.parseDouble(careerNavbarList[1])
                    widthh = Math.abs(v1-u1)
                    heightt = Math.abs(v2-u2)
                    def roi2 =ROIs.createEllipseROI(v1,v2,widthh,heightt,plane)
                    d1 = roi2.getShape()
                    def annotation1 = PathObjects.createAnnotationObject(roi2)
                    annotation1.setColorRGB(getColorRGB(0,102,0))
                    //annotation1.name= textId.concat(textname)             
                    addObject(annotation1)                                         
                }
               if(c==0){
                    def v1 = X
                    def v2 = Y
                    careerNavbarList.add(v1.toString())
                    careerNavbarList.add(v2.toString())
                    c =c+1
                }
               }
            }
            tmp_points_list.add(new Point2(X, Y))         
        }
        if(c==1){
            //Cleared
            careerNavbarList.clear()
    
        }
        if(c==0){
    
            def roi = new PolygonROI(tmp_points_list)
            def annotation = new PathAnnotationObject(roi)
             // Set the class here below
            annotation.setPathClass(annotationClass)
    
            annotation.setColorRGB(getColorRGB(0,255,0))
            //annotation.name= textId.concat(textname)
            hierarchy.addPathObject(annotation, false)
        }
        c = 0

    }
}
fireHierarchyUpdate()
print "Done!"



