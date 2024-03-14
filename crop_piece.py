import cv2 as cv
import numpy as np
from sgfication import img_functions as imf

def crop_piece(board_img_fn, piece_img_fn):

    # Load the image
    #board_img = cv.imread(str(board_img_fn))
    #board_img_gray = cv.cvtColor(board_img, cv.COLOR_BGR2GRAY)

    piece_img = cv.imread(str(piece_img_fn))
    piece_img_gray = cv.cvtColor(piece_img, cv.COLOR_BGR2GRAY)

    row_spacing, column_spacing = imf.get_all_spacing(board_img_fn)

    #find circle and get center. if we can't find circle, get intersection.
    #   then simply use the spacing as the bounding box for this

    circles = imf.find_circles(piece_img_fn, row_spacing, column_spacing)

    if circles is not None:
        #get biggest circle
        circle=max(circles,key=lambda r: r[2])
        x, y, _ = circle

        print('circles')

    else:

        intersections = imf.find_intersections(piece_img_fn, keep_intermediate=False)

        #if we have multiple, we can use one closest to image center as heuristic
        img_center = (piece_img_gray.shape[1] // 2, piece_img_gray.shape[0] // 2)
        centerest_intersection = min(intersections, key=lambda p: (p[0] - img_center[0])**2 + (p[1] - img_center[1])**2)

        x, y = centerest_intersection

        print('intersections')
    
    
    print(f"x {x} y {y} ")
    print(f"x dim {piece_img_gray.shape[1]} y dim {piece_img_gray.shape[0]}")

    #now crop it with bounding box centered on this spot
    #   maxes and mins to ensure we don't go outside image boundaries
    
    crop_left = max( 0 ,  int(x - column_spacing // 2) )
    crop_right = min( int(crop_left + column_spacing) , piece_img_gray.shape[1] )
    crop_top = max( 0 , int(y - row_spacing // 2) )
    crop_bottom = min( int(crop_top + row_spacing) , piece_img_gray.shape[0] )

    #debug
    print(f"left {crop_left} right {crop_right} top {crop_top} bottom {crop_bottom}")

    # IF SCREENSHOT ISN"T BIG ENOUGH, RETURN ERROR THAT SCREENSHOT NEEDS TO BE BIGGER

    cropped_img = piece_img[crop_top:crop_bottom, crop_left:crop_right]

    cv.imwrite('cropped_piece.png', cropped_img)

import sys
crop_piece(sys.argv[1],sys.argv[2])