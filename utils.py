import cv2 as cv
import numpy as np

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
    (cX,cY) = (w //2, h//2)

    # grab the rotation matrix, then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv.getRotationMatrix2D((cX, cY), angle, 1.0)
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

# distinguish rectangle and diamond
def genRectAndDiam(im):
    rectangles = np.zeros((im.shape[0],im.shape[0],1), np.uint8)
    diamonds = np.zeros((im.shape[0],im.shape[0],1), np.uint8)
    
    _, blob_contours, _ = cv.findContours(im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in blob_contours:
        actualArea = cv.contourArea(contour)
        _, _, w, h = cv.boundingRect(contour)
        boundingArea = w * h
        if (actualArea / boundingArea > 0.75):	# rectangular
            rectangles = cv.fillPoly(rectangles, contour, (255,255,255))
        else:	# diamond
            diamonds = cv.fillPoly(diamonds, contour, (255,255,255))

    return rectangles, diamonds