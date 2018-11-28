import argparse
from utils import *
from draw import draw

SMALL_REGION_REMOVAL_THRESHOLD = 1000
OPEN_SMALL_REGION_REMOVAL = 350  # 350
ARROW_OPEN_RADIUS = 12
CANNY_THRESHOLD_1 = 100
CANNY_THRESHOLD_2 = 100
CANNY_APETURE_SIZE = 3
HOUGH_THRESHOLD = 100
HOUGH_MIN_LINE_LENGTH = 30
HOUGH_MAX_LINE_GAP = 5
BLOCK_SIZE = 65
DILATE_KERNEL_SIZE = 2
ERODE_KERNEL = 10


def gen_code(im_name):
    im = cv.imread(im_name)
    # resize image for faster processing
    resize_im = resize_image(im)
    # cv.imwrite(im_name[:-4]+"_resize.jpg", resize_im)
    gray_im = cv.cvtColor(resize_im, cv.COLOR_BGR2GRAY)
    # cv.imwrite(im_name[:-4]+"_gray.jpg", gray_im)
    binarize_im = cv.adaptiveThreshold(
        gray_im, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, BLOCK_SIZE, 40)
    # cv.imwrite(im_name[:-4]+"_bina.jpg", binarize_im)
    bitwise_im = cv.bitwise_not(binarize_im)
    # cv.imwrite(im_name[:-4]+"_bitwise.jpg", bitwise_im)
    dilate_kernel = np.ones(
        (DILATE_KERNEL_SIZE * 2 + 1, DILATE_KERNEL_SIZE * 2 + 1), np.uint8)
    dilate_im = cv.dilate(bitwise_im, dilate_kernel)
    # cv.imwrite(im_name[:-4]+"_dilate.jpg", dilate_im)
    denoise_im = denoiseAndFill(dilate_im, SMALL_REGION_REMOVAL_THRESHOLD)
    # cv.imwrite(im_name[:-4]+"_denoise.jpg", denoise_im)
    edge_im = cv.Canny(denoise_im, CANNY_THRESHOLD_1,
                       CANNY_THRESHOLD_2, CANNY_APETURE_SIZE)
    # cv.imwrite(im_name[:-4]+"_edge.jpg", edge_im)
    lines = cv.HoughLinesP(edge_im, 1, np.pi/180, HOUGH_THRESHOLD,
                           HOUGH_MIN_LINE_LENGTH, HOUGH_MAX_LINE_GAP)
    angle = get_rotate_angle(lines)
    rotated_im = rotate_image(angle, denoise_im)
    # cv.imwrite(im_name[:-4]+"_rotated.jpg", rotated_im)

    fill_im = fillContour(rotated_im)
    # cv.imwrite(im_name[:-4]+"_fill.jpg", fill_im)

    kernel = np.ones((ARROW_OPEN_RADIUS * 2 + 1,
                      ARROW_OPEN_RADIUS * 2 + 1), np.uint8)
    opening_im = cv.morphologyEx(fill_im, cv.MORPH_OPEN, kernel)
    # cv.imwrite(im_name[:-4]+"_opening.jpg", opening_im)

    diff_im = cv.absdiff(fill_im, opening_im)
    # cv.imwrite(im_name[:-4]+"_diff.jpg", diff_im)

    arrows_im = denoiseAndFill(diff_im, OPEN_SMALL_REGION_REMOVAL)
    # cv.imwrite(im_name[:-4]+"_arrows.jpg", arrows_im)
    _, arrow_contours, _ = cv.findContours(
        arrows_im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    arrow_lst = sort_arrow(arrow_contours)

    blob_im = cv.absdiff(fill_im, arrows_im)
    # cv.imwrite(im_name[:-4]+"_blob.jpg", blob_im)

    shape_lst = []

    # find circles
    kernel = np.ones((ERODE_KERNEL * 2 + 1, ERODE_KERNEL * 2 + 1), np.uint8)
    erode_blob_im = cv.erode(blob_im, kernel, iterations=1)
    blob_boundary_im = cv.absdiff(blob_im, erode_blob_im)
    # cv.imwrite(im_name[:-4]+"_blob_boundary.jpg", blob_boundary_im)
    _, blob_contours, _ = cv.findContours(
        blob_boundary_im, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # print(len(blob_contours))
    remain_contours, circle_lst = detectCircle(
        blob_contours, blob_im.shape[0], blob_im.shape[1])
    shape_lst += circle_lst
    # print(len(circle_lst), len(remain_contours))
    # cv.imwrite(im_name[:-4]+"_circles.jpg", circles_im)
    remain_contours, elip_lst = detectEllipse(
        blob_contours, blob_im.shape[0], blob_im.shape[1])
    shape_lst += elip_lst

    remain_contours, rhombus_lst = detectRhombus(
        blob_contours, blob_im.shape[0], blob_im.shape[1])
    shape_lst += rhombus_lst
    # get rectangles and diamonds
    remain_contours, blob_lst = detectRectAndDiam(
        remain_contours, blob_im.shape[0], blob_im.shape[1])
    shape_lst += blob_lst
    # print(len(blob_lst), len(remain_contours))
    for contour in remain_contours:
        x, y, w, h = cv.boundingRect(contour)
        shape_lst.append(Shape_and_the_contour(
            Shape.rectangle, contour, (x + w//2, y + h//2)))
    sorted_shape_lst = sort_shape(shape_lst)

    # sorted_shape_lst, code = draw_node(sorted_shape_lst)
    code = draw(sorted_shape_lst, arrow_lst)
    return code


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test.')
    parser.add_argument('-i', '--image', required=True,
                        help='Path to the image')

    args = parser.parse_args()
    im_name = args.image

    # im_name = "test4.jpg"

    print(gen_code(im_name))
