import cv2 as cv
import numpy as np
from sgfication import img_functions as imf

def crop_piece(board_img_fn, piece_img_fn, outfile='cropped_piece.png', debug_outfile='debug_output.png'):
    
    piece_img = cv.imread(str(piece_img_fn))
    piece_img_gray = cv.cvtColor(piece_img, cv.COLOR_BGR2GRAY)
    
    row_spacing, column_spacing = imf.get_all_spacing(board_img_fn)
    
    circles = imf.find_circles(piece_img_fn, row_spacing, column_spacing,min_circle_dist=0)
    
    debug_img = piece_img.copy()
    
    if circles is not None:
        circle = max(circles, key=lambda r: r[2])  # Get largest circle
        x, y, r = circle
        cv.circle(debug_img, (x, y), 1, (0, 255, 0), -1)  # Draw detected center
        cv.circle(debug_img, (x, y), r, (0, 255, 0), 1)  # Draw detected circle
        print('Detected circles')
    else:
        intersections = imf.find_intersections(piece_img_fn, keep_intermediate=False)
        img_center = (piece_img_gray.shape[1] // 2, piece_img_gray.shape[0] // 2)
        centerest_intersection = min(intersections, key=lambda p: (p[0] - img_center[0])**2 + (p[1] - img_center[1])**2)
        x, y = centerest_intersection
        cv.circle(debug_img, (x, y), 5, (255, 0, 0), -1)  # Draw detected intersection
        print('Detected intersections')
    
    print(f"x: {x}, y: {y}")
    print(f"Image dims - x: {piece_img_gray.shape[1]}, y: {piece_img_gray.shape[0]}")
    
    crop_left = max(0, int(x - column_spacing // 2))
    crop_right = min(int(crop_left + column_spacing), piece_img_gray.shape[1])
    crop_top = max(0, int(y - row_spacing // 2))
    crop_bottom = min(int(crop_top + row_spacing), piece_img_gray.shape[0])
    
    print(f"Cropping bounds - left: {crop_left}, right: {crop_right}, top: {crop_top}, bottom: {crop_bottom}")
    
    # Draw bounding box on debug image
    #cv.rectangle(debug_img, (crop_left, crop_top), (crop_right, crop_bottom), (0, 0, 255), 2)
    
    cropped_img = piece_img[crop_top:crop_bottom, crop_left:crop_right]
    
    cv.imwrite(outfile, cropped_img)
    cv.imwrite(debug_outfile, debug_img)  # Save debug visualization