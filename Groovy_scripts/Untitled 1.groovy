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
def rotated = false
def server = QP.getCurrentImageData().getServer()
def h = server.getHeight()
def w = server.getWidth()
print(w)
print(h)