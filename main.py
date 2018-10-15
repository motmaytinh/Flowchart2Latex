import cv2 as cv
import argparse

CANNY_THRESHOLD_1 = 100
CANNY_THRESHOLD_2 = 100
CANNY_APETURE_SIZE = 3

def main():
    parser = argparse.ArgumentParser(description='Test.')
    parser.add_argument('--name', help='name for image')

    args = parser.parse_args()
    im_name = args.name

    im = cv.imread(im_name)
    gray_im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    cv.imwrite(im_name[:-4]+"_gray.jpg", gray_im)
    binarize_im = cv.adaptiveThreshold(gray_im, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 65, 40)
    cv.imwrite(im_name[:-4]+"_bina.jpg", binarize_im)
    bitwise_im = cv.bitwise_not(binarize_im)
    cv.imwrite(im_name[:-4]+"_bitwise.jpg", bitwise_im)
    edge_im = cv.Canny(bitwise_im, CANNY_THRESHOLD_1, CANNY_THRESHOLD_2, CANNY_APETURE_SIZE)
    cv.imwrite(im_name[:-4]+"_edge.jpg", edge_im)


if __name__ == '__main__':
    main()
