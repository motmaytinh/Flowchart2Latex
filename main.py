import cv2 as cv
import numpy as np
import argparse

SMALL_REGION_REMOVAL_THRESHOLD = 310
OPEN_SMALL_REGION_REMOVAL = 350
ARROW_OPEN_RADIUS = 12
CANNY_THRESHOLD_1 = 100
CANNY_THRESHOLD_2 = 100
CANNY_APETURE_SIZE = 3
HOUGH_THRESHOLD = 200
HOUGH_MIN_LINE_LENGTH = 30
HOUGH_MAX_LINE_GAP = 5

def main():
    parser = argparse.ArgumentParser(description='Test.')
    parser.add_argument('--name', help='name for image')

    args = parser.parse_args()
    im_name = args.name

    im = cv.imread(im_name)
    gray_im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    # cv.imwrite(im_name[:-4]+"_gray.jpg", gray_im)
    binarize_im = cv.adaptiveThreshold(gray_im, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 65, 40)
    # cv.imwrite(im_name[:-4]+"_bina.jpg", binarize_im)
    bitwise_im = cv.bitwise_not(binarize_im)
    # cv.imwrite(im_name[:-4]+"_bitwise.jpg", bitwise_im)
    denoise_im = denoiseAndFill(bitwise_im, SMALL_REGION_REMOVAL_THRESHOLD)

    edge_im = cv.Canny(denoise_im, CANNY_THRESHOLD_1, CANNY_THRESHOLD_2, CANNY_APETURE_SIZE)
    # cv.imwrite(im_name[:-4]+"_edge.jpg", edge_im)
    lines = cv.HoughLinesP(edge_im, 1, np.pi/180, HOUGH_THRESHOLD, HOUGH_MIN_LINE_LENGTH, HOUGH_MAX_LINE_GAP)
    # print(lines.shape)
    # blank_image = np.zeros((im.shape[0],im.shape[0],1), np.uint8)
    angle = get_rotate_angle(lines)
    rotated_im = rotate_image(angle, edge_im)
    # cv.imwrite(im_name[:-4]+"_rotated.jpg", rotated_im)

    fill_im = fillContour(rotated_im)
    # cv.imwrite(im_name[:-4]+"_fill.jpg", fill_im)

    kernel = np.ones((ARROW_OPEN_RADIUS * 2 + 1,ARROW_OPEN_RADIUS  * 2 + 1), np.uint8)
    opening_im = cv.morphologyEx(fill_im, cv.MORPH_OPEN, kernel)
    # cv.imwrite(im_name[:-4]+"_opening.jpg", opening_im)

    diff_im = cv.absdiff(fill_im, opening_im)
    # cv.imwrite(im_name[:-4]+"_diff.jpg", diff_im)

    arrows_im = denoiseAndFill(diff_im, OPEN_SMALL_REGION_REMOVAL)
    # cv.imwrite(im_name[:-4]+"_arrows.jpg", arrows_im)

    shapes_im = cv.absdiff(rotated_im, opening_im)
    # cv.imwrite(im_name[:-4]+"_arrows.jpg", arrows_im)
    
    # get rectangles and diamonds
    blob_im = cv.absdiff(fill_im, arrows_im)
    # cv.imwrite(im_name[:-4]+"_blob.jpg", blob_im)

    # find circles
    kernel = np.ones((21,21),np.uint8)
    erode_blob_im = cv.erode(blob_im,kernel,iterations = 1)
    blob_boundary_im = cv.absdiff(blob_im, erode_blob_im)
    # cv.imwrite(im_name[:-4]+"_blob_boundary.jpg", blob_boundary_im)
    _, blob_contours, _ = cv.findContours(blob_boundary_im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    circles_blob = np.zeros((rotated_im.shape[0],rotated_im.shape[1]), np.uint8)

    for contour in blob_contours:
        temp = np.zeros((im.shape[0],im.shape[0],1), np.uint8)
        circContour = []
        circContour.append(contour)
        cv.drawContours(temp, circContour, -1, (255,255,255), 3)
        circle = cv.HoughCircles(temp,cv.HOUGH_GRADIENT,2,im.shape[0]//4,
                                param1=200,param2=100,minRadius=0,maxRadius=0)
        if circle is not None:
            print("aha")
            circles_blob = cv.fillPoly(circles_blob, contour, (255,255,255))
    # cv.imwrite(im_name[:-4]+"_circles.jpg", circles_blob)
    print(blob_boundary_im.shape, circles_blob.shape)
    circle_remv = cv.absdiff(blob_boundary_im, circles_blob)

    rectangles, diamonds = genRectAndDiam(circle_remv)

    cv.imwrite(im_name[:-4]+"_rectangles.jpg", rectangles)
    cv.imwrite(im_name[:-4]+"_diamond.jpg", diamonds)
    


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

def denoiseAndFill(im, thres):
    _, contours, _ = cv.findContours(im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for i in range(len(contours)):
        if cv.contourArea(contours[i]) < thres:
            # im = cv.fillPoly(im, pts=contour, color=(0,0,0))
            im = cv.drawContours(im, contours, i, (0,0,0), -1)
    
    return im

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

if __name__ == '__main__':
    main()
