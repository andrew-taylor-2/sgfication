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

        #FILL REST HERE 

    else:
        #get biggest circle
        circle=max(circles,key=lambda x: x[2])
        x, y, _ = circle
    
    #now crop it with bounding box centered on this spot
    
    crop_left = x - column_spacing // 2
    crop_right = crop_left + column_spacing
    crop_top = y - row_spacing // 2
    crop_bottom = crop_top + row_spacing

    # IF SCREENSHOT ISN"T BIG ENOUGH, RETURN ERROR THAT SCREENSHOT NEEDS TO BE BIGGER

    cropped_img = piece_img[crop_top:crop_bottom, crop_left:crop_right]

    cv.imwrite('cropped_piece.png', cropped_img)