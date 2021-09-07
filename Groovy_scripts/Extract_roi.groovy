import qupath.lib.gui.dialogs.Dialogs
import qupath.lib.scripting.QP
import qupath.lib.images.writers.TileExporter
import qupath.lib.geom.Point2
import qupath.lib.roi.PolygonROI
import qupath.lib.objects.PathAnnotationObject
import qupath.lib.images.servers.ImageServer
import qupath.lib.roi.ROIs
import qupath.lib.regions.ImagePlane
import qupath.lib.roi.RoiTools
import qupath.lib.objects.PathObjects




//Aperio Image Scope displays images in a different orientation
//def rotated = true

println("***********************************")
println("***********************************")
println("*Qupath Application for Bio-imaging*")
println("***********************************")
println("***********************************")

def choice1 = 256.0
def roi = getSelectedROI()
def xaxis = 0
def yaxis = 0 
def server = QP.getCurrentImageData().getServer()
def height = server.getHeight()
def width = server.getWidth()


if(roi!=null){
    def d = roi.getShape()
    xaxis = d.getX()
    yaxis = d.getY()
    width = d.getX()+roi.getBoundsWidth()
    height = d.getY()+roi.getBoundsHeight()
}   

print(xaxis)
print(yaxis)
print(width)
print(height)
print("Done")

