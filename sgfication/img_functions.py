import argparse
import numpy as np
import cv2 as cv


def get_all_spacing(image_path):
    """Takes in go board image, finds intersections, and then gets spacing between them.""" 

    from statistics import mode
    intersections = find_intersections(image_path)
    rows, columns = group_intersections_by_axis(intersections)
    row_distances = calculate_spacing(rows)
    column_distances = calculate_spacing(columns)
    
    # Use mode to find the most common distance, assuming minor variations
    row_spacing = mode(row_distances)
    column_spacing = mode(column_distances)
    
    #print(f"Row spacing: {row_spacing}, Column spacing: {column_spacing}")

    return row_spacing, column_spacing


def find_intersections(image_path, keep_intermediate=False, return_corners=False):
    """Uses opencv probabilistic Hough Lines to find intersections."""

    # Step 1: Read the image
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Step 1.5: smooth for more regular edges
    blurred = cv.GaussianBlur(gray, (5,5), 0)

    if keep_intermediate:
        #debug
        cv.imwrite('blurred.png',blurred)

    # Step 2: Edge detection
    edges = cv.Canny(blurred, 50, 150, apertureSize=3)

    if keep_intermediate:
        #debug
        cv.imwrite('edges.png',edges)

    # Step 2.5: dilate and erode
    dilated = cv.dilate(edges, None, iterations=2)

    edges = cv.erode(dilated, None, iterations=3)

    #the dilation and erosion is good for finding lines, it won't be as good for finding circles

    if keep_intermediate:
        #debug
        cv.imwrite('edges_erodil.png',edges)

    # Step 3: Line detection
    #lines = cv.HoughLines(edges, 1, np.pi / 180, 300)
    #300 is a good starting place, underestimates slightly. 
    #might need to use 300, check intersections, if i don't get enough, then decrease
    #this isn't working very well on a dense board

    #could try houghlines probabilistic
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=20, maxLineGap=5)

    # i think the probabilistic isn't sampling enough, still getting weird false negatives. need to find out why. 

    # Preparing to find intersections
    intersections = []
    corners = []
    if lines is not None:
        for i in range(len(lines)):
            for j in range(i+1, len(lines)):
                line1 = lines[i][0]
                line2 = lines[j][0]

                if are_vertical_and_horizontal(line1, line2):
                    intersection, is_corner = segment_intersection(line1, line2, 3, 3)
                    if is_corner:
                        corners.append(intersection)
                    elif intersection:
                        intersections.append(intersection)
    
    if keep_intermediate:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        #debug
        cv.imwrite('prob_houghlines.png', img)

    if keep_intermediate:
        # Display intersections on the image
        for x, y in intersections:
            cv.circle(img, (x, y), radius=3, color=(0, 0, 255), thickness=-1)        
        for x, y in corners:
            cv.circle(img, (x, y), radius=3, color=(255, 0, 0), thickness=-1)

        cv.imwrite('intersections.png', img)
    if return_corners:
        return intersections, corners
    else:
        intersections.extend(corners)
        return intersections


def group_intersections_by_axis(intersections):
    # Separate intersections into rows and columns based on their coordinates
    rows = {}
    columns = {}
    for x, y in intersections:
        # Group by y-coordinate for rows
        if y not in rows:
            rows[y] = []
        rows[y].append((x, y))
        
        # Group by x-coordinate for columns
        if x not in columns:
            columns[x] = []
        columns[x].append((x, y))
    
    # While the above works, it seems inefficient to store both x and y when one of them is the key. still, this does 
    #   make for less clunky looking code

    # Sort intersections in each row and column
    for k in rows:
        rows[k].sort(key=lambda coord: coord[0])  # Sort by x-coordinate
    for k in columns:
        columns[k].sort(key=lambda coord: coord[1])  # Sort by y-coordinate
    
    return rows, columns


def calculate_spacing(rows_or_columns):
    distances = []
    for intersections in rows_or_columns.values():
        for i in range(len(intersections) - 1):
            dist = np.linalg.norm(np.array(intersections[i]) - np.array(intersections[i + 1]))
            distances.append(dist)
    return distances



def match_asset_to_board(large_image_path, small_image_paths,return_matched_region=False):

    """finds best match and location out of multiple small images. Will help to decide which assets to use."""
    
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
    


def find_matches(board_img_path, template_img_path, threshold=0.8):
    board_img = cv.imread(board_img_path, 0)  # Load the board image in grayscale
    template_img = cv.imread(template_img_path, 0)  # Load the template image in grayscale
    w, h = template_img.shape[::-1]  # Get the dimensions of the template

    # Perform template matching
    res = cv.matchTemplate(board_img, template_img, cv.TM_CCOEFF_NORMED) # Should I blur first?
    loc = np.where(res >= threshold)

    matches = []
    for pt in zip(*loc[::-1]):  # Switch x and y coordinates
        matches.append(pt)
        # Optional: for visualization
        cv.rectangle(board_img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    
    # Optional: Show the result
    cv.imshow('Detected', board_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return matches

def get_lowest_index(matches):

    lowest_x, _ =min(matches,key = lambda x: x[0])
    _, lowest_y =min(matches,key = lambda x: x[1])

    return lowest_x, lowest_y

def consolidate_matches(matches, row_spacing, col_spacing, lowest_x, lowest_y):
    
    # When we use cv.matchTemplate, we'll get a cluster of matches around the "true" match location, since 
    #   a slight shift in position might not be enough to stop two images from matching. 

    # Therefore, we need to consolidate these matches. Luckily for us, the matches come in dense clusters -- 
    #   the space between clusters is much larger than the width/height of the clusters.

    # So what we can do is use our row/column spacing and "round" the match locations to integer multiples of this.

    # We need one more trick, which is to subtract all x and y by the first match's x and y. This is to prevent the
    #   arbitrarily-sized non-board space on the edges from causing our clusters to fall along the midpoint between 
    #   row and column multiples, which would make points within one cluster get sent (rounded) to multple row/column locations.
    #   This works because of the dense clusters.

    # use a set to avoid duplicate grid positions
    consolidated_grid = set()
    consolidated_board = set()


    for x, y in matches:
        # round to get index on board
        board_x = round( ( x - lowest_x ) / col_spacing)
        board_y = round( ( y - lowest_y ) / row_spacing)

        #get idealized grid coordinates 
        grid_x = board_x * col_spacing
        grid_y = board_y * row_spacing

        consolidated_grid.add((grid_x, grid_y))
        consolidated_board.add((board_x, board_y))

    # now that we've eliminated duplicates, we would rather work with a list
    return list(consolidated_board), list(consolidated_grid)

#HMMM the lowest x and lowest y will differ based on whether im matching black white or intersection... 
# I can output lowest x,y and correct grid positions later, but is this too weird and clunky? nah honestly that's
#   probably for the best. this is kind of like transforming vox2world, doing something, then going back world2vox


def find_circles(image_path, row_spacing, column_spacing, keep_intermediate=True):

    #recycling this from intersections code

    # Step 1: Read the image
    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Step 1.5: smooth for more regular edges
    blurred = cv.GaussianBlur(gray, (5,5), 0)

    if keep_intermediate:
        #debug
        cv.imwrite('blurred.png',blurred)

    # Step 2: Edge detection
    edges = cv.Canny(blurred, 50, 150, apertureSize=3)

    if keep_intermediate:
        #debug
        cv.imwrite('edges.png',edges)

    #the erosion and dilations don't help with the circles

    # Step 3: Circle detection

    #we're going to use spacing info to bound piece size
    average_spacing=(row_spacing + column_spacing) / 2
    upper_bound_piece_radius= np.round(   (average_spacing/2) * 1.05  ).astype("int")
    lower_bound_piece_radius= np.round(   (average_spacing/2) * 0.8   ).astype("int")

    #min circle distance is based on spacing as well
    min_circle_dist=average_spacing * 0.9 

    #could try houghlines probabilistic (i have good values for size bounds, so I'm setting param2 a little lower)
    circles = cv.HoughCircles(edges, cv.HOUGH_GRADIENT, 1, min_circle_dist, param1=50, param2=20, minRadius=lower_bound_piece_radius, maxRadius=upper_bound_piece_radius)

    #put circles on image
    if circles is not None:
        # get circle params as integers
        circles = np.round(circles[0, :]).astype("int")    

        for (x, y, r) in circles:
            cv.circle(img, (x, y), r, (0, 255, 0), 2)
    
    cv.imwrite('circles.png', img)
    return circles

# Helper functions section

def segment_intersection(line1, line2, tolerance=1, corner_tolerance=None):
    # need to find intersections this way rather than something more intuitive like using slopes
    #   because we could run into trouble with infinite slopes (in fact, half of the slopes that 
    #   interest us are infinite)

    # set corner_tolerance if we want to check for corners

    # Unpack line segment endpoints
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    
    # Calculate denominators
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    
    # Check if lines are parallel (denominator == 0)
    if den == 0:
        return None, None  # No intersection
    
    # Calculate intersection point
    px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / den
    py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / den
    
    # Check if the intersection point is within both line segments, allowing wiggle room
    #   Need wiggle room because otherwise line endpoint touching other line segment might not be found
    if min(x1, x2) - tolerance <= px <= max(x1, x2) + tolerance and \
        min(y1, y2) - tolerance <= py <= max(y1, y2) + tolerance and \
        min(x3, x4) - tolerance <= px <= max(x3, x4) + tolerance and \
        min(y3, y4) - tolerance <= py <= max(y3, y4) + tolerance:
        intersection = (int(px), int(py))
    else:
        intersection = None
    
    # optionally check cornerness (note that, due to conditionals, corner_tolerance more than intersection tolerance is unhelpful)
    if corner_tolerance and intersection is not None:
        #check if one of the endpoints touches intersection for each segment
        if ( abs(px-x1) <= corner_tolerance and abs(py-y1) <= corner_tolerance ) ^ \
            ( abs(px-x2) <= corner_tolerance and abs(py-y2) <= corner_tolerance ) and \
            ( abs(px-x3) <= corner_tolerance and abs(py-y3) <= corner_tolerance ) ^ \
            ( abs(px-x4) <= corner_tolerance and abs(py-y4) <= corner_tolerance ):

            is_corner=True

        else:
            is_corner=False
    
        return intersection, is_corner
    
    else:
        return intersection, None


def are_vertical_and_horizontal(line1, line2, tolerance=5):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    #just check distance in each dim (slope approach doesn't play well with vertical and horizontal lines)
    vertical = (abs(x2 - x1) < tolerance , abs(x4 - x3) < tolerance)
    horizontal = (abs(y2 - y1) < tolerance , abs(y4 - y3) < tolerance)

    if (vertical[0] and horizontal[1]) or (vertical[1] and horizontal[0]):
        return True
    else:
        return False

    #might want to base tolerance off image size; these tolerances are kind of large for min line seg length of 20


if __name__ == '__main__':

    #IVE MADE SOME CHANGES AND NEED TO UPDATE ARGPARSER

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

    #parser for getting spacing
    parser_get_all_spacing = subparsers.add_parser('get_all_spacing', help='Find the row and column spacing.')
    parser_get_all_spacing.add_argument('image_path', type=str, help='Path to the image for which we want row and column spacing')

    args = parser.parse_args()

    if args.command == 'find_best_match':
        if not args.output:
            best_match_index, location = match_asset_to_board(args.large_image_path, args.small_image_paths)
            print(f"Small image {best_match_index} is the best match, located at: {location}")
        else:
            best_match_index, location, matched_region_image = match_asset_to_board(args.large_image_path, args.small_image_paths, return_matched_region=True)
            cv.imwrite(args.output, matched_region_image)
            print(f"Matched region saved to {args.output}")

    elif args.command == 'find_intersections':
        find_intersections(args.image_path)
    
    elif args.command == 'get_all_spacing':
        get_all_spacing(args.image_path)

