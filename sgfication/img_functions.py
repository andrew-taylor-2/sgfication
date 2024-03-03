import argparse
import numpy as np
import cv2 as cv


def find_best_match_location(large_image_path, small_image_paths,return_matched_region=False):
    
    # load the large image and convert it to grayscale. 
    large_image_np = cv.imread(large_image_path,cv.IMREAD_GRAYSCALE)
    
    # initialize variables to keep track of the best match
    best_match_value = -np.inf
    best_match_location = None
    best_match_index = None
    
    for i, small_image_path in enumerate(small_image_paths):
        # load the small image, convert it to grayscale
        small_image_np = cv.imread(small_image_path,cv.IMREAD_GRAYSCALE)
        
        # perform NCC
        result = cv.matchTemplate(large_image_np, small_image_np, cv.TM_CCORR_NORMED)
        
        # find the peak value and its location
        _, max_value, _, max_loc = cv.minMaxLoc(result)
        
        # check if this result is better than what we've seen before
        if max_value > best_match_value:
            best_match_value = max_value
            #top_left_y, top_left_x = np.unravel_index(np.argmax(result), result.shape)
            best_match_top_left = max_loc
            #this line isn't necessary, let's see if i need it for later...
            best_match_index = i

    if return_matched_region:
        # output matched region
        kernel_w, kernel_h = small_image_np.shape
        matched_region = large_image_np[best_match_top_left[1]:best_match_top_left[1]+kernel_h, best_match_top_left[0]:best_match_top_left[0] + kernel_w]
        matched_region_image = cv.cvtColor(matched_region, cv.COLOR_GRAY2BGR)

        return best_match_index, best_match_location, matched_region_image
    else:
        # return the index of the best matching small image and its location
        return best_match_index, best_match_location


# if called from terminal
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find which of the smaller images is contained in the larger image and its location.')
    parser.add_argument('large_image_path', type=str, help='Path to the large image')
    parser.add_argument('small_image_paths', type=str, nargs='+', help='Path to the small images')
    parser.add_argument("--output", type=str, help="Optional: Path to save the output image of the matched region.")

    args = parser.parse_args()

    if not args.output:
        best_match_index, location = find_best_match_location(args.large_image_path, args.small_image_paths)
    else:
        best_match_index, location, matched_region_image = find_best_match_location(args.large_image_path, args.small_image_paths, return_matched_region=True)
        cv.imwrite(args.output, matched_region_image)
        print(f"Matched region saved to {args.output}")
    
    print(f"Small image {best_match_index} is the best match, located at: {location}")