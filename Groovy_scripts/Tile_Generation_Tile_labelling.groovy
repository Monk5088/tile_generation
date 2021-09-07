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


root_path = "C:\\Digital_Histopathology\\Tile_generation"

//Aperio Image Scope displays images in a different orientation
def rotated = false

println("***********************************")
println("***********************************")
println("*Qupath Application for Bio-imaging*")
println("***********************************")
println("***********************************")


//def choice1 = Dialogs.showChoiceDialog("My title", 
//        "Please make your choice",
//        [256.0],
//        256.0)
//print "You chose $choice1"
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

path = server.getURIs().getAt(0).getPath()

scnpath = path.substring(1,path.lastIndexOf("."))+".scn"

xmlfile = path.substring(1, path.lastIndexOf(".")) + ".xml"  // HERE

File inputfile = new File(root_path +"\\"+"inputfile.txt")

inputfile.write("")
inputfile.append(scnpath+"\n")
inputfile.append(xmlfile+"\n")
inputfile.append(xaxis+" "+yaxis+" "+width+" "+height+"\n")
inputfile.append(choice1+"\n")

print("Done")

task1path = "$root_path"+"\\"+"createfolder.py"
print("$task1path")

def task1 = "python $task1path 1".execute()
task1.waitFor()

task2_path ="$root_path"+"\\"+"main"+"\\"+"main.py"
def task2 = "python $task2_path 1".execute()
task2.waitFor()

Dialogs.showPlainMessage("Message",
"""
The tiling process is done. 

""")

task3_path = "$root_path"+"\\"+"read_master_info_file.py"
def task3 = "python $task3_path".execute()
task3.waitFor()
print(task3.text)

print("Done")