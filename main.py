import cv2 as cv
import numpy as np
import argparse

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
    edge_im = cv.Canny(bitwise_im, CANNY_THRESHOLD_1, CANNY_THRESHOLD_2, CANNY_APETURE_SIZE)
    # cv.imwrite(im_name[:-4]+"_edge.jpg", edge_im)
    lines = cv.HoughLinesP(edge_im, 1, np.pi/180, HOUGH_THRESHOLD, HOUGH_MIN_LINE_LENGTH, HOUGH_MAX_LINE_GAP)
    # print(lines.shape)
    # blank_image = np.zeros((im.shape[0],im.shape[0],1), np.uint8)
    angle = get_rotate_angle(lines)
    rotated_im = rotate_image(angle, edge_im)

    
    cv.imwrite(im_name[:-4]+"_rotated.jpg", rotated_im)


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
    a,_ = np.histogram(angle, bins=36, range=(-90,90),density=False)
    return np.where(a == max(a))[0] * 5 - 90

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

if __name__ == '__main__':
    main()
