import cv2
import sys, getopt, os

CG_ERR = -1
CG_HELP = 0

def helpmsg(state, msg=''):
    global CG_ERR, CG_HELP
    out_msg = 'Usage: python flipFrames.py -i <inputfolder> -o <outputfolder>'
    if state == CG_ERR:
        out_msg = "[Err] %s" % out_msg
        print out_msg
        sys.exit(2)
    elif state == CG_HELP:
        print out_msg
        sys.exit()

infolder = ''
outfolder = ''

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifolder=", "ofolder="])
except getopt.GetoptError:
    helpmsg(CG_ERR)

for opt, arg in opts:
    if opt == '-h':
        helpmsg(CG_HELP)
    elif opt in ("-i", "--ifolder"):
        infolder = arg
    elif opt in ("-o", "--ofolder"):
        outfolder = arg
 
if not infolder or not outfolder:
    helpmsg(CG_ERR)

filenames = os.listdir(infolder)

count = 0
for f in filenames:
    infile = os.path.join(infolder, f)
    outfile = os.path.join(outfolder, "flipped_%s" % f)
    try:
        img = cv2.imread(infile)
        flipped_img = cv2.flip(img, 1)
        cv2.imwrite(outfile, flipped_img)
        count += 1
    except:
        print "Ignoring file: %s" % infile
        # print "Unexpected error:", sys.exc_info()[0]

print "Flipped %d frames" % count

