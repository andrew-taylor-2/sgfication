import cv2 as cv
import numpy as np
from sgfication import img_functions as imf

def crop_piece(board_img, piece_img):
    row_spacing, column_spacing = imf.get_all_spacing(board_img)

    #find circle and get center. if we can't find circle, get intersection.
    #   then simply use the spacing as the bounding box for this

    circles = imf.find_circles(piece_img, row_spacing, column_spacing)

    if not circles:
        intersections, corners = imf.find_intersections(board_img, keep_intermediate=False, only_perpendicular=True)

        #for now we can consider interesctions and corners together
        intersections.append(corners)

        #if we have multiple, we can use one closest to image center as heuristic
        img_center = (piece_img.shape[1] // 2, piece_img.shape[0] // 2)
        centerest_intersection = min(intersections, key=lambda p: (p[0] - img_center[0])**2 + (p[1] - img_center[1])**2)

        x, y = centerest_intersection

    else:
        #get biggest circle
        circle=max(circles,key=lambda r: r[2])
        x, y, _ = circle
    
    #now crop it with bounding box centered on this spot
    #   maxes and mins to ensure we don't go outside image boundaries
    
    crop_left = max( 0 ,  x - column_spacing // 2 )
    crop_right = min( crop_left + column_spacing , piece_img.shape[1] )
    crop_top = max( 0 , y - row_spacing // 2 )
    crop_bottom = min( crop_top + row_spacing , piece_img.shape[0] )

    # IF SCREENSHOT ISN"T BIG ENOUGH, RETURN ERROR THAT SCREENSHOT NEEDS TO BE BIGGER

    cropped_img = piece_img[crop_top:crop_bottom, crop_left:crop_right]

    cv.imwrite('cropped_piece.png', cropped_img)