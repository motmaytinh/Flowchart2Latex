import cv2 as cv
import numpy as np
from enum_type import *

W = 1000

def resize_image(image):
    height, width, depth = image.shape
    imgScale = W/width
    newX, newY = image.shape[1]*imgScale, image.shape[0]*imgScale
    newimg = cv.resize(image,(int(newX),int(newY)))
    return newimg

# detect main angle in an image
def get_rotate_angle(lines):
    """
    Calculate rotation angle for tilted image by detect major angle in image
    Divide angle by bin of 5 degree
    Choose the bin with larget count
    """
    angle = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            angle.append(np.degrees(np.arctan((y2-y1)/(x2-x1))))
    a,_ = np.histogram(angle, bins=72, range=(-90,90),density=False)
    return np.where(a == max(a))[0] * 2.5 - 90

# enlarge image border and rotate the content
def rotate_image(angle, im):
    # grab the dimensions of the image and then determine the center
    (h,w) = im.shape[:2]
    (cX,cY) = (w//2, h//2)

    # grab the rotation matrix, then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv.getRotationMatrix2D((cX, cY), angle[0], 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # perform the actual rotation and return the image
    M[0,2] += (nW / 2) - cX
    M[1,2] += (nH / 2) - cY

    return cv.warpAffine(im, M, (nW, nH))

# fill out small noise
def denoiseAndFill(im, thres):
    _, contours, _ = cv.findContours(im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for i in range(len(contours)):
        if cv.contourArea(contours[i]) < thres:
            # im = cv.fillPoly(im, pts=contour, color=(0,0,0))
            im = cv.drawContours(im, contours, i, (0,0,0), -1)
    
    return im

# white filling blob
def fillContour(im):
    _, contours, _ = cv.findContours(im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for i in range(len(contours)):
        im = cv.drawContours(im, contours, i, (255,255,255), -1)

    return im

def detectCircle(blob_contours, im_width, im_height):
    circles_blob = np.zeros((im_width, im_height), np.uint8)
    circles_lst = []

    for contour in blob_contours:
        temp = np.zeros((im_width,im_height,1), np.uint8)
        circContour = []
        circContour.append(contour)
        cv.drawContours(temp, circContour, -1, (255,255,255), 3)
        circle = cv.HoughCircles(temp,cv.HOUGH_GRADIENT,2,im_width//4,
                                param1=200,param2=100,minRadius=0,maxRadius=0)
        if circle is not None:
            print("aha")
            circles_lst.append(Shape_and_the_coordinate(Shape.circle, contour))
            circles_blob = cv.fillPoly(circles_blob, contour, (255,255,255))

    return circles_blob, circles_lst

# distinguish rectangle and diamond
def genRectAndDiam(im):
    rectangles = np.zeros((im.shape[0],im.shape[0],1), np.uint8)
    diamonds = np.zeros((im.shape[0],im.shape[0],1), np.uint8)
    shape_lst = []

    _, blob_contours, _ = cv.findContours(im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in blob_contours:
        actualArea = cv.contourArea(contour)
        _, _, w, h = cv.boundingRect(contour)
        boundingArea = w * h
        if (actualArea / boundingArea > 0.75):	# rectangular
            rectangles = cv.fillPoly(rectangles, contour, (255,255,255))
            shape_lst.append(Shape_and_the_contour(Shape.rectangle, contour))
        else:	# diamond
            diamonds = cv.fillPoly(diamonds, contour, (255,255,255))
            shape_lst.append(Shape_and_the_contour(Shape.diamond, contour))

    return rectangles, diamonds, shape_lst

def sort_contours(shape_lst):

    # construct the list of bounding boxes and sort them from top to bottom
    boundingBoxes = [cv.boundingRect(c.get_cnts()) for c in shape_lst]
    (cnts, boundingBoxes) = zip(*sorted(zip(shape_lst, boundingBoxes), key=lambda b: b[1][1]))

    # return the list of sorted contours and bounding boxes
    return cnts, boundingBoxes

