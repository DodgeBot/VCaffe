import numpy as np
import cv2
import sys, getopt, os
from time import sleep
import time
import imutils
import random

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

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def onLeftSide(l, p):
    x1, y1 = l[0]
    x2, y2 = l[1]
    x, y = p
    v1 = (x2 - x1, y2 - y1)
    v2 = (x2 - x, y2 - y)
    cross_product = v1[0]*v2[1] - v1[1]*v2[0]
    if cross_product >= 0:
        return False
    else:
        return True

G_LABEL_RIGHT = 0
G_LABEL_STRAIGHT = 1
G_LABEL_LEFT = 2

def decideLabel(scores):
    l = scores[0]
    m = scores[1]
    r = scores[2]

    if m <= 1:
        return G_LABEL_STRAIGHT
    if min(l, m, r) == m:
        return G_LABEL_STRAIGHT
    elif min(l, r) == l:
        return G_LABEL_LEFT
    else:
        return G_LABEL_RIGHT


def decideAction(img, rects, thickness=1, color=(0, 255, 0)):
    # params for scoring
    SIZE_PENALTY = 10000 # for each 10000, add 1 penalty score

    # scores for each section
    scores = [0, 0, 0]

    # draw section divider
    color_d = (0, 0, 255)
    thick_d = 3
    iw = img.shape[1]
    ih = img.shape[0]
    
    # set ratio for central section on upper and lower edge
    upper_center_ratio = 1.0/5.0
    lower_center_ratio = 1.0/3.0

    # set section pivot points
    upper = int(iw/2.0 - upper_center_ratio*iw/2.0)
    lower = int(iw/2.0 - lower_center_ratio*iw/2.0)
    x11 = upper
    x12 = lower
    x21 = iw - upper
    x22 = iw - lower
    l1 = [(x11, 0), (x12, ih)]
    l2 = [(x21, 0), (x22, ih)]

    # cv2.line(img, l1[0], l1[1], color_d, thick_d)
    # cv2.line(img, l2[0], l2[1], color_d, thick_d)

    for x, y, w, h in rects:
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        color_no_pad = (255, 255, 255)
        thickness_no_pad = 3

        # rect out the human
        # cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), color, thickness)
        
        # calculate area
        w_draw = w - 2*pad_w
        h_draw = h - 2*pad_h
        area = w_draw * h_draw

        # center of the human
        center = (x+int(0.5*w), y+int(0.5*h)) 
        # print(center)

        # decide which section the point belongs to
        left1 = onLeftSide(l1, center)
        left2 = onLeftSide(l2, center)
        if left1:
            idx = 0
        elif left2:
            idx = 1
        else:
            idx = 2

        # score for appearance
        scores[idx] += 1
        # score for area size
        scores[idx] += area/SIZE_PENALTY 

        # cv2.circle(img, center, 1, color_no_pad, thickness_no_pad)
    
    # warning_h = int(ih/2)
    # warning_points = [(10, warning_h), (int(iw/2), warning_h), (iw-60, warning_h)]
    # for i in [0, 1, 2]:
    #     cv2.putText(img, "s: %d" % scores[i], warning_points[i], cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_d, 2)
    
    label = decideLabel(scores)
    # if label == G_LABEL_RIGHT:
    #     text = "Right"
    # elif label == G_LABEL_STRAIGHT:
    #     text = "Straight"
    # else:
    #     text = "Left"
    # cv2.putText(img, text, (int(iw/2-5), int(ih/2+100)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_d, 2)
    return label


# def draw_detection(img, rects, thickness=1, color=(0, 255, 0)):
#     print('')
#     
#     # draw section divider
#     color_d = (0, 0, 255)
#     thick_d = 3
#     iw = img.shape[1]
#     ih = img.shape[0]
#     
#     # set ratio for central section on upper and lower edge
#     upper_center_ratio = 1.0/5.0
#     lower_center_ratio = 1.0/3.0
# 
#     print(upper_center_ratio)
# 
#     upper = int(iw/2.0 - upper_center_ratio*iw/2.0)
#     lower = int(iw/2.0 - lower_center_ratio*iw/2.0)
#     x11 = upper
#     x12 = lower
#     x21 = iw - upper
#     x22 = iw - lower
# 
#     cv2.line(img, (x11, 0), (x12, ih), color_d, thick_d)
#     cv2.line(img, (x21, 0), (x22, ih), color_d, thick_d)
# 
#     for x, y, w, h in rects:
#         pad_w, pad_h = int(0.15*w), int(0.05*h)
#         color_no_pad = (255, 255, 255)
#         thickness_no_pad = 3
# 
#         # rect out the human
#         cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), color, thickness)
# 
#         # center of the human
#         center = (x+int(0.5*w), y+int(0.5*h)) 
#         print(center)
#         cv2.circle(img, center, 1, color_no_pad, thickness_no_pad)

if __name__ == '__main__':
    # HOGDescriptor
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    test_stat = [0, 0, 0]
    
    ftrain = open(os.path.join(outfolder, 'train.txt'), 'a')
    ftest = open(os.path.join(outfolder, 'test.txt'), 'a')

    cap = cv2.VideoCapture(infile)
    timestamp = int(time.time())
    counter = 0
    while True:
        label = 0 # 0, 1, 2
        _, img = cap.read()
        if img is None:
            break
	img = imutils.resize(img, width=min(600, img.shape[1]))
        found, w = hog.detectMultiScale(img, winStride=(8, 8), padding=(32,32), scale=1.05)

        label = decideAction(img, found)
        img = cv2.resize(img, (256, 256))
        # writing files and print label for pipe
        if random.randint(1, 10) <= 3:
            test_or_train = 'test'
        else:
            test_or_train = 'train'
        outfile = os.path.join(outfolder, test_or_train, "%d_cam1_%d_%d.jpg" % (timestamp, counter, label))
    	cv2.imwrite(outfile, img)
        # print(outfile + ' ' + str(label))
        if test_or_train == 'test':
            ftest.write(outfile + ' ' + str(label) + '\n')
        else:
            ftrain.write(outfile + ' ' + str(label) + '\n')
        
        # for flipped img
        img = cv2.flip(img, 1)
        if label == G_LABEL_RIGHT:
            label = G_LABEL_LEFT
        elif label == G_LABEL_LEFT:
            label = G_LABEL_RIGHT
        # writing files and print label for pipe
        if random.randint(1, 10) <= 3:
            test_or_train = 'test'
        else:
            test_or_train = 'train'
        outfile = os.path.join(outfolder, test_or_train, "f_%d_cam1_%d_%d.jpg" % (timestamp, counter, label))
    	cv2.imwrite(outfile, img)
        if test_or_train == 'test':
            ftest.write(outfile + ' ' + str(label) + '\n')
        else:
            ftrain.write(outfile + ' ' + str(label) + '\n')
        # if label == 0:
        #     test_stat[0] += 1
        # elif label == 1:
        #     test_stat[1] += 1
        # else:
        #     test_stat[2] += 1

        # s = sum(test_stat)
        # print("%.2f, %.2f, %.2f," % (test_stat[0] / float(s) * 100, test_stat[1] / float(s) * 100, test_stat[2] / float(s) * 100))

        # cv2.imshow("feed", img)
        # cv2.waitKey(0)

        counter += 1
        sys.stdout.write("\rFrame %d" % counter)
        sys.stdout.flush()
        
        # ch = 0xFF & cv2.waitKey(1)
        # if ch == 27:
        #     break

    print('')
    ftrain.close()
    ftest.close()
    cap.release()
    cv2.destroyAllWindows()
