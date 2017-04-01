import cv2
import sys, getopt, os

CG_ERR = -1
CG_HELP = 0

def helpmsg(state, msg=''):
    global CG_ERR, CG_HELP
    out_msg = 'Usage: python video2img.py -i <inputfile> -o <outputfolder>'
    if state == CG_ERR:
        out_msg = "[Err] %s" % out_msg
        print out_msg
        sys.exit(2)
    elif state == CG_HELP:
        print out_msg
        sys.exit()

infile = ''
outfolder = ''

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=", "ofolder="])
except getopt.GetoptError:
    helpmsg(CG_ERR)

for opt, arg in opts:
    if opt == '-h':
        helpmsg(CG_HELP)
    elif opt in ("-i", "--ifile"):
        infile = arg
    elif opt in ("-o", "--ofolder"):
        outfolder = arg

if not infile or not outfolder:
    helpmsg(CG_ERR)


vidcap = cv2.VideoCapture(infile)
# vidcap = cv2.VideoCapture('../videos/170112/left00.MOV')
success,image = vidcap.read()
count = 0
success = True
outfile = ''
while success:
    success,image = vidcap.read()
    # print 'Read a new frame: ', success
    outfile = os.path.join(outfolder, "frame%d.jpg" % count)
    cv2.imwrite(outfile, image)
    # cv2.imwrite("../images/frame%d.jpg" % count, image)     # save frame as JPEG file
    count += 1
# remove last frame, which is likely to be broken
os.remove(outfile)
print "Coverted to %d frame(s)" % count

