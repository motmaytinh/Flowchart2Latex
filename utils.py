import cv2 as cv
import numpy as np
from enum_type import *

W = 1000


def resize_image(image):
    height, width, depth = image.shape
    imgScale = W/width
    newX, newY = image.shape[1]*imgScale, image.shape[0]*imgScale
    newimg = cv.resize(image, (int(newX), int(newY)))
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
        for x1, y1, x2, y2 in line:
            angle.append(np.degrees(np.arctan((y2-y1)/(x2-x1 + 1))))
    a, _ = np.histogram(angle, bins=72, range=(-90, 90), density=False)
    return np.where(a == max(a))[0] * 2.5 - 90


# enlarge image border and rotate the content
def rotate_image(angle, im):
    # grab the dimensions of the image and then determine the center
    (h, w) = im.shape[:2]
    (cX, cY) = (w//2, h//2)

    # grab the rotation matrix, then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv.getRotationMatrix2D((cX, cY), angle[0], 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # perform the actual rotation and return the image
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    return cv.warpAffine(im, M, (nW, nH))


# fill out small noise
def denoiseAndFill(im, thres):
    _, contours, _ = cv.findContours(
        im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        if cv.contourArea(contours[i]) < thres:
            # im = cv.fillPoly(im, pts=contour, color=(0,0,0))
            im = cv.drawContours(im, contours, i, (0, 0, 0), -1)

    return im


# white filling blob
def fillContour(im):
    _, contours, _ = cv.findContours(
        im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    im = cv.drawContours(im, contours, -1, (255, 255, 255), -1)

    return im


def detectRhombus(blob_contours, im_width, im_height):
    remain_contours = []
    rhombus_lst = []
    # count = 0

    for contour in blob_contours:
        x, y, w, h = cv.boundingRect(contour)

        temp = np.zeros((im_width, im_height, 1), np.uint8)
        rhombusContour = []
        rhombusContour.append(contour)
        cv.drawContours(temp, rhombusContour, -1, (255, 255, 255), 3)

        # Translate
        Mt = np.float32([[1, 0, -x], [0, 1, -y]])
        temp = cv.warpAffine(temp, Mt, (2*w, h))

        temp = cv.flip(temp, 1)
        # cv.imwrite(str(count)+'b'+'.jpg',temp)
        # Shear
        # a = cv.contourArea(contour)
        # Sx = w/h-a/(h*h)
        # print(Sx)
        Ms = np.float32([[1, -0.5, 0], [0, 1, 0]])
        temp = cv.warpAffine(temp, Ms, (2*w, h))

        # cv.imwrite(str(count)+'.jpg',temp)

        # count += 1

        _, tmpcontours, _ = cv.findContours(
            temp, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # print(len(contour))
        tmpcontour = tmpcontours[0]
        _, _, w2, h2 = cv.boundingRect(tmpcontour)
        boundingArea = w2*h2
        actualArea = cv.contourArea(tmpcontour)

        if actualArea/boundingArea > 0.8:
            rhombus_lst.append(Shape_and_the_contour(
                Shape.rhombus, contour, (x + w//2, y + h//2)))
        else:
            remain_contours.append(contour)

    return remain_contours, rhombus_lst


def detectEllipse(blob_contours, im_width, im_height):
    remain_contours = blob_contours
    ellipse_lst = []
    count = 0
    for contour in blob_contours:
        x, y, w, h = cv.boundingRect(contour)

        temp = np.zeros((im_width, im_height, 1), np.uint8)
        elipContour = []
        elipContour.append(contour)
        cv.drawContours(temp, elipContour, -1, (255, 255, 255), 3)

        if w > h:
            temp = cv.resize(temp, (int(im_width*h/w), im_height))
            # cv.imwrite('elip' + str(count) + '.jpg', temp)
            count += 1
            circle = cv.HoughCircles(temp, cv.HOUGH_GRADIENT, 2, im_width//4,
                                     param1=200, param2=100, minRadius=0, maxRadius=0)

            if circle is not None:
                # print('aha')
                ellipse_lst.append(Shape_and_the_contour(
                    Shape.ellipse, contour, (x + w//2, y + h//2)))
                remain_contours.remove(contour)

    return remain_contours, ellipse_lst


def detectCircle(blob_contours, im_width, im_height):
    remain_contours = blob_contours
    circles_lst = []

    for contour in blob_contours:
        temp = np.zeros((im_width, im_height, 1), np.uint8)
        circContour = []
        circContour.append(contour)
        cv.drawContours(temp, circContour, -1, (255, 255, 255), 3)
        circle = cv.HoughCircles(temp, cv.HOUGH_GRADIENT, 2, im_width//4,
                                 param1=200, param2=100, minRadius=0, maxRadius=0)
        if circle is not None:
            # print("Circle")
            x, y, w, h = cv.boundingRect(contour)
            circles_lst.append(Shape_and_the_contour(
                Shape.circle, contour, (x + w//2, y + h//2)))
            remain_contours.remove(contour)

    return remain_contours, circles_lst

# distinguish rectangle and diamond


def detectRectAndDiam(blob_contours, im_width, im_height):
    remain_contours = blob_contours
    shape_lst = []

    for contour in blob_contours:
        x, y, w, h = cv.boundingRect(contour)
        actualArea = cv.contourArea(contour)
        boundingArea = w * h
        if (actualArea / boundingArea > 0.7):  # rectangular
            shape_lst.append(Shape_and_the_contour(
                Shape.rectangle, contour, (x + w//2, y + h//2)))
            remain_contours.remove(contour)
        else:  # diamond
            shape_lst.append(Shape_and_the_contour(
                Shape.diamond, contour, (x + w//2, y + h//2)))
            remain_contours.remove(contour)

    return remain_contours, shape_lst


def sort_shape(shape_lst):
    # construct the list of bounding boxes and sort them from top to bottom
    lst = sorted(shape_lst, key=lambda x: x.get_center()
                 [0] + x.get_center()[1])
    sorted_shape_lst = []
    for i in range(len(lst)):
        lst[i].set_name('shape' + str(i))
        sorted_shape_lst.append(lst[i])

    # return the list of sorted contours and bounding boxes
    return sorted_shape_lst


def sort_arrow(arrow_contours):
    lst = []
    for arrow in arrow_contours:
        x, y, w, h = cv.boundingRect(arrow)
        direction = "horizontal" if w > h else "vertical"
        lst.append(Arrow(direction, arrow, (x + w//2, y + h//2)))
    sorted_arrow_lst = sorted(lst, key=lambda x: x.get_center()[
                              0] + x.get_center()[1])
    return sorted_arrow_lst
