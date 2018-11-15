import argparse
from utils import *

SMALL_REGION_REMOVAL_THRESHOLD = 1000
OPEN_SMALL_REGION_REMOVAL = 450 #350
ARROW_OPEN_RADIUS = 12
CANNY_THRESHOLD_1 = 100
CANNY_THRESHOLD_2 = 100
CANNY_APETURE_SIZE = 3
HOUGH_THRESHOLD = 200
HOUGH_MIN_LINE_LENGTH = 30
HOUGH_MAX_LINE_GAP = 5
BLOCK_SIZE = 65
DILATE_KERNEL_SIZE = 1

def main():
    parser = argparse.ArgumentParser(description='Test.')
    parser.add_argument('--name', help='name for image')

    args = parser.parse_args()
    im_name = args.name

    im = cv.imread(im_name)
    # resize image for faster processing
    resize_im = resize_image(im)
    # cv.imwrite(im_name[:-4]+"_resize.jpg", resize_im)
    gray_im = cv.cvtColor(resize_im, cv.COLOR_BGR2GRAY)
    # cv.imwrite(im_name[:-4]+"_gray.jpg", gray_im)
    binarize_im = cv.adaptiveThreshold(gray_im, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, BLOCK_SIZE, 40)
    # cv.imwrite(im_name[:-4]+"_bina.jpg", binarize_im)
    bitwise_im = cv.bitwise_not(binarize_im)
    # cv.imwrite(im_name[:-4]+"_bitwise.jpg", bitwise_im)
    dilate_kernel = np.ones((DILATE_KERNEL_SIZE * 2 + 1, DILATE_KERNEL_SIZE * 2 + 1), np.uint8)
    dilate_im = cv.dilate(bitwise_im, dilate_kernel)
    # cv.imwrite(im_name[:-4]+"_dilate.jpg", dilate_im)
    denoise_im = denoiseAndFill(dilate_im, SMALL_REGION_REMOVAL_THRESHOLD)
    cv.imwrite(im_name[:-4]+"_denoise.jpg", denoise_im)
    # edge_im = cv.Canny(denoise_im, CANNY_THRESHOLD_1, CANNY_THRESHOLD_2, CANNY_APETURE_SIZE)
    # cv.imwrite(im_name[:-4]+"_edge.jpg", edge_im)
    # lines = cv.HoughLinesP(edge_im, 1, np.pi/180, HOUGH_THRESHOLD, HOUGH_MIN_LINE_LENGTH, HOUGH_MAX_LINE_GAP)
    # # print(lines.shape)
    # # blank_image = np.zeros((im.shape[0],im.shape[0],1), np.uint8)
    # angle = get_rotate_angle(lines)
    # rotated_im = rotate_image(angle, edge_im)
    # # cv.imwrite(im_name[:-4]+"_rotated.jpg", rotated_im)

    # fill_im = fillContour(rotated_im)
    # # cv.imwrite(im_name[:-4]+"_fill.jpg", fill_im)

    # kernel = np.ones((ARROW_OPEN_RADIUS * 2 + 1,ARROW_OPEN_RADIUS  * 2 + 1), np.uint8)
    # opening_im = cv.morphologyEx(fill_im, cv.MORPH_OPEN, kernel)
    # # cv.imwrite(im_name[:-4]+"_opening.jpg", opening_im)

    # diff_im = cv.absdiff(fill_im, opening_im)
    # # cv.imwrite(im_name[:-4]+"_diff.jpg", diff_im)

    # arrows_im = denoiseAndFill(diff_im, OPEN_SMALL_REGION_REMOVAL)
    # # cv.imwrite(im_name[:-4]+"_arrows.jpg", arrows_im)

    # shapes_im = cv.absdiff(rotated_im, opening_im)
    # # cv.imwrite(im_name[:-4]+"_shapes.jpg", arrows_im)
    
    # # get rectangles and diamonds
    # blob_im = cv.absdiff(fill_im, arrows_im)
    # # cv.imwrite(im_name[:-4]+"_blob.jpg", blob_im)

    # # find circles
    # kernel = np.ones((21,21),np.uint8)
    # erode_blob_im = cv.erode(blob_im,kernel,iterations = 1)
    # blob_boundary_im = cv.absdiff(blob_im, erode_blob_im)
    # cv.imwrite(im_name[:-4]+"_blob_boundary.jpg", blob_boundary_im)
    # _, blob_contours, _ = cv.findContours(blob_boundary_im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # circles_blob = np.zeros((rotated_im.shape[0],rotated_im.shape[1]), np.uint8)

    # for contour in blob_contours:
    #     temp = np.zeros((im.shape[0],im.shape[0],1), np.uint8)
    #     circContour = []
    #     circContour.append(contour)
    #     cv.drawContours(temp, circContour, -1, (255,255,255), 3)
    #     circle = cv.HoughCircles(temp,cv.HOUGH_GRADIENT,2,im.shape[0]//4,
    #                             param1=200,param2=100,minRadius=0,maxRadius=0)
    #     if circle is not None:
    #         print("aha")
    #         circles_blob = cv.fillPoly(circles_blob, contour, (255,255,255))
    # cv.imwrite(im_name[:-4]+"_circles.jpg", circles_blob)
    # print(blob_boundary_im.shape, circles_blob.shape)
    # circle_remv = cv.absdiff(blob_boundary_im, circles_blob)

    # rectangles, diamonds = genRectAndDiam(circle_remv)

    # cv.imwrite(im_name[:-4]+"_rectangles.jpg", rectangles)
    # cv.imwrite(im_name[:-4]+"_diamond.jpg", diamonds)


if __name__ == '__main__':
    main()
