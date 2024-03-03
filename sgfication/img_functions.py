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
    

def find_intersections(image_path):
    from numpy.linalg import LinAlgError

    # Step 1: Read the image
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Step 2: Edge detection
    edges = cv.Canny(gray, 50, 150, apertureSize=3)

    #debug
    cv.imwrite('edges.png',edges)

    # Step 3: Line detection
    lines = cv.HoughLines(edges, 1, np.pi / 180, 300)
    #300 is a good starting place, underestimates slightly. 
    #might need to use 300, check intersections, if i don't get enough, then decrease
    #this isn't working very well on a dense board

    #could try houghlines probabilistic
    #lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=5)

    # Preparing to find intersections
    if lines is not None:
        lines = [l[0] for l in lines]  # Extracting line information
        intersections = []
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                rho1, theta1 = lines[i]
                rho2, theta2 = lines[j]

                # Calculate intersection
                A = np.array([
                    [np.cos(theta1), np.sin(theta1)],
                    [np.cos(theta2), np.sin(theta2)]
                ])
                b = np.array([[rho1], [rho2]])
                try:
                    x0, y0 = np.linalg.solve(A, b)
                    
                    #check if solver is giving us overflow or if it's type conversion
                    if x0.__abs__()>10000 or y0.__abs__()>10000:
                        print('yep')

                        #yes, solver is giving very large values

                    x0, y0 = int(np.round(x0)), int(np.round(y0))

                    #some of these are way too extreme so let's cut off things
                    if x0.__abs__()<10000 and y0.__abs__()<10000:
                        intersections.append((x0, y0))

                except LinAlgError:
                    # parallel lines will give singular matrix and error
                    # better way to fix this could be to group lines based on slope 
                    #   and then only find intersections between lines with significantly different slope
                    pass

        # Display intersections on the image
        for x, y in intersections:
            cv.circle(img, (x, y), radius=3, color=(0, 255, 0), thickness=-1)

        cv.imshow('Intersections', img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        print("No lines were detected.")


if __name__ == '__main__':
    # create a subparser to handle different commands
    parser = argparse.ArgumentParser(description='Image processing utilities')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Parser for finding best match location
    parser_find_best_match = subparsers.add_parser('find_best_match', help='Find which of the smaller images is contained in the larger image and its location.')
    parser_find_best_match.add_argument('large_image_path', type=str, help='Path to the large image')
    parser_find_best_match.add_argument('small_image_paths', type=str, nargs='+', help='Path to the small images')
    parser_find_best_match.add_argument("--output", type=str, help="Optional: Path to save the output image of the matched region.")

    # parser for finding intersections
    parser_find_intersections = subparsers.add_parser('find_intersections', help='Find intersections in the given image.')
    parser_find_intersections.add_argument('image_path', type=str, help='Path to the image for finding intersections')

    args = parser.parse_args()

    if args.command == 'find_best_match':
        if not args.output:
            best_match_index, location = find_best_match_location(args.large_image_path, args.small_image_paths)
            print(f"Small image {best_match_index} is the best match, located at: {location}")
        else:
            best_match_index, location, matched_region_image = find_best_match_location(args.large_image_path, args.small_image_paths, return_matched_region=True)
            cv.imwrite(args.output, matched_region_image)
            print(f"Matched region saved to {args.output}")

    elif args.command == 'find_intersections':
        find_intersections(args.image_path)