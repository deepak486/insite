import sys
print "THIS SCRIPT IS DEPRECATED -- inSite can now read CC XML files directly"
sys.exit()

#
# extract camera positions from a ContextCapture exported XML file
# written by andrew.chapman@auav.com.au Sept 2017
#
# Files are XML, we keep track of what block nesting level of interest we're in as it cascades down:
#
# 			<Photo>
# ...
# 					<Center>
# 						<x>151.24333883988933</x>
# 						<y>-33.753288283968935</y>
# 						<z>160.56979423481971</z>
#
# NOTE WHEN EXPORTING THE BlocksExchange XML file from CC:
# - export SRS needs to be set to WGS84 (EPSG: 4326)
# - export rotation format 'Yaw, Pitch, Roll angles'
#


import os
import copy
import string
import argparse

# command line argument parsing
# NOTE: because of a windows bug with python arg parsing, you need to call this script with "python SCRIPTNAME" rather than just "SCRIPTNAME" in the windows command terminal
parser = argparse.ArgumentParser(description='Convert CC BlocksExchange XML to inSite cameras file format')
parser.add_argument('--height_offset', type=float, help='Height offset to shift positions within inSite')
parser.add_argument('inputfile',  help='path to CC XML input file')
parser.add_argument('outputfile', help='path to output insite cameras file')
parser.add_argument('source_image_path', help='Path to images used within the XML file')
parser.add_argument('dest_image_path',   help='Path to images to write to insite cameras file')
args = parser.parse_args()

# EDIT PROJECT VALUES HERE -- modify later to be passed in as parameters
imageSearch  = args.source_image_path   # e.g. 'H:/DATA2/05-01-18_Kooralbyn 5/'
imageReplace = args.dest_image_path     # e.g. 'DATA/Demo/Kooralbyn_Rail_Bridge/model/photos/'
vertOffset   = 0.0                      # e.g. 34.31 
if args.height_offset:   
	vertOffset = args.height_offset
filenameIn  = args.inputfile;           # e.g. 'H:\DATA2\CC_Kooralbyn_5\cameras_for_insite.xml'
filenameOut = args.outputfile;          # e.g. 'H:\DATA2\DEV\inSite\DATA\Demo\Kooralbyn_Rail_Bridge\model\cameras.js'

inPhotoBlock    = False
inMetadataBlock = False
inCenterBlock   = False
inRotationBlock = False

allCams = []

class Camera():
	image = ""
	rot = [0,0,0]
	pos = [0,0,0]

tempCam = Camera()

# loop through each line in the XML file, looking for features we want and keeping track of nesting
lines = open(filenameIn, 'r').readlines()
for line in lines:
	if not inPhotoBlock and "<Photo>" in line:
		inPhotoBlock  = True
		tempCam.pos   = [0,0,0]
		tempCam.rot   = [0,0,0]
		tempCam.image = ""
	if "</Photo>" in line:
		inPhotoBlock = False
	if inPhotoBlock and "<Metadata>" in line:
		inMetadataBlock = True
	if "</Metadata>" in line:
		inMetadataBlock = False
	if inPhotoBlock and not inMetadataBlock and "<Rotation>" in line:
		inRotationBlock = True
	if inPhotoBlock and not inMetadataBlock and "</Rotation>" in line:
		inRotationBlock = False
	if inPhotoBlock and not inMetadataBlock and "<Center>" in line:
		inCenterBlock = True
	if inPhotoBlock and not inMetadataBlock and "</Center>" in line:
		inCenterBlock = False
	if inPhotoBlock and "<ImagePath>" in line:
		tempCam.image = line[line.find("<ImagePath>")+11:line.find("</ImagePath>")]
		tempCam.image = string.replace(tempCam.image, imageSearch, imageReplace)
	if inRotationBlock and "<Yaw>" in line:
		tempCam.rot[0] = line[line.find("<Yaw>")+5:line.find("</Yaw>")]
	if inRotationBlock and "<Pitch>" in line:
		tempCam.rot[1] = line[line.find("<Pitch>")+7:line.find("</Pitch>")]
	if inRotationBlock and "<Roll>" in line:
		tempCam.rot[2] = line[line.find("<Roll>")+6:line.find("</Roll>")]
	if inCenterBlock and "<x>" in line:
		tempCam.pos[0] = line[line.find("<x>")+3:line.find("</x>")]
	if inCenterBlock and "<y>" in line:
		tempCam.pos[1] = line[line.find("<y>")+3:line.find("</y>")]
	if inCenterBlock and "<z>" in line:
		tempCam.pos[2] = line[line.find("<z>")+3:line.find("</z>")]
	if inPhotoBlock and not inMetadataBlock and "</Center>" in line:
		inCenterBlock = False
		print "Found camera: " + tempCam.image
		print "  Rotation:   " + `tempCam.rot`
		print "  Position:   " + `tempCam.pos`
		allCams.append(copy.deepcopy(tempCam))

print "Total number of camera positions found: " + `len(allCams)`
print "Saving to file: " + filenameOut

outfile = open(filenameOut, 'w')

# loop through out list of cameras, writing them out to the output file
for cam in allCams:
	s = """
    viewer.entities.add({
    image : "%s",
    position : Cesium.Cartesian3.fromDegrees(%s,%s,%f),
    
    hpr : Cesium.HeadingPitchRoll.fromDegrees(%f,%f,%f),
    inSiteType : "cameraPosition",
    show : false,
    point : {
        pixelSize : 6,
        color : Cesium.Color.BLUE,
    },
    //cylinder : { length : 1.0, topRadius : 0.0, bottomRadius : 0.1, material : Cesium.Color.RED.withAlpha(0.3) },
    //polyline : {
    //	positions: [Cesium.Cartesian3.fromElements(0,0,0), Cesium.Cartesian3.fromElements(0,0,1)]
    //},
    });""" % (cam.image, 
    cam.pos[0],cam.pos[1],float(cam.pos[2])+vertOffset, 
    #cam.pos[0],cam.pos[1],float(cam.pos[2])+vertOffset, 
    #float(cam.rot[0])-90,float(cam.rot[1])+90,cam.rot[2])
	float(cam.rot[0]),float(cam.rot[1]),float(cam.rot[2]))
	#print s
	outfile.write(s);



# we will also write out a command file, for easy re-running of this conversion in the event of later format updates
outfile = open(filenameOut + ".cmd", 'w')
outfile.write("python " + os.path.basename(__file__) + " ")
if args.height_offset:
	outfile.write("--height_offset " + `args.height_offset` + " ")
outfile.write("\"" + args.inputfile + "\" \"" + args.outputfile + "\" \"" + args.source_image_path + "\" \"" + args.dest_image_path + "\"")
