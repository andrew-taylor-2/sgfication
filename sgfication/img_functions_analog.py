import cv2
import numpy as np

## first commented area is old approach, new one begins below
##these functions will help me generalize the algo.
#
## I need a procedure for what to do when I can't detect edges or find a rectangle
##    I think first I'll try more blur, but then I'll probably default to what I'm doing now -- hope it's a screenshot
#
#def four_point_transform(image, pts):
#    # Obtain a consistent order of the points and unpack them
#    rect = order_points(pts)
#    (tl, tr, br, bl) = rect
#
#    # Compute the width and height of the new image
#    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
#    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
#    maxWidth = max(int(widthA), int(widthB))
#
#    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
#    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
#    maxHeight = max(int(heightA), int(heightB))
#
#    # Set the destination points for the perspective transform
#    dst = np.array([
#        [0, 0],
#        [maxWidth - 1, 0],
#        [maxWidth - 1, maxHeight - 1],
#        [0, maxHeight - 1]], dtype="float32")
#
#    # Compute the perspective transform matrix and apply it
#    M = cv2.getPerspectiveTransform(rect, dst)
#    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
#
#    return warped
#
#def order_points(pts):
#    # Initialize a list of coordinates that will be ordered
#    rect = np.zeros((4, 2), dtype="float32")
#
#    # The top-left point will have the smallest sum,
#    # the bottom-right will have the largest sum
#    s = pts.sum(axis=1)
#    rect[0] = pts[np.argmin(s)]
#    rect[2] = pts[np.argmax(s)]
#
#    # The top-right point will have the smallest difference,
#    # the bottom-left will have the largest difference
#    diff = np.diff(pts, axis=1)
#    rect[1] = pts[np.argmin(diff)]
#    rect[3] = pts[np.argmax(diff)]
#
#    return rect
#
#def detect_board_edges(image):
#    # Convert to grayscale
#    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#    
#    # Apply GaussianBlur to reduce noise and improve edge detection
#    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#    
#    # Use Canny edge detector
#    edged = cv2.Canny(blurred, 50, 150)
#
#    # Find contours
#    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#    # Assume the largest contour is the board
#    if len(contours) == 0:
#        return None
#    
#    largest_contour = max(contours, key=cv2.contourArea)
#
#    # Approximate the contour to a polygon
#    peri = cv2.arcLength(largest_contour, True)
#    approx = cv2.approxPolyDP(largest_contour, 0.02 * peri, True)
#
#    # If the polygon has 4 vertices, we have found the board
#    if len(approx) == 4:
#        return approx.reshape((4, 2))
#
#    return None
#
##if __name__=='__main__':
##    import sys
##    import os
##    # Example usage:
##    image = cv2.imread(sys.argv[1])
##    board_edges = detect_board_edges(image)
##
##    if board_edges is not None:
##        warped = four_point_transform(image, board_edges)
##        cv2.imshow("Warped", warped)
##        cv2.waitKey(0)
##        cv2.destroyAllWindows()
##    else:
##        print("Board edges not detected")




## begin claude response which is clearly wrong at certain points

import cv2
import numpy as np
import math

#class GoBoardDetector:
#    def __init__(self, debug=False):
#        self.debug = debug

def preprocess_image( image):
    """
        Preprocess the input image for board detection
        Args:
            image (np.ndarray): Input image
        Returns:
            np.ndarray: Preprocessed grayscale image
        """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to handle different lighting conditions
    thresh = cv2.adaptiveThreshold(
            gray, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 
            81,8
        )
    
    return thresh

def find_board_contours( preprocessed_image):
    """
        Find potential board contours
        Args:
            preprocessed_image (np.ndarray): Preprocessed image
        Returns:
            list: Sorted contours by area
        """
    # Find contours
    contours, _ = cv2.findContours(
            preprocessed_image, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
    
    # Sort contours by area, largest first
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    # Filter for quadrilateral shapes
    board_candidates = []
    for contour in sorted_contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            # Look for quadrilateral with 4 points
            if len(approx) == 4:
                board_candidates.append(approx)
    
    return board_candidates

def order_points( pts):
    """
        Order points for perspective transform (top-left, top-right, bottom-right, bottom-left)
        Args:
            pts (np.ndarray): Input points
        Returns:
            np.ndarray: Ordered points
        """
    rect = np.zeros((4, 2), dtype="float32")
    
    # Top-left will have smallest sum, bottom-right largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # Top-right will have smallest difference, bottom-left largest
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect
import cv2
import numpy as np
import cv2
import numpy as np

def perspective_transform(image, points, scale=1.0):
    """
    Apply perspective transform to straighten board with an adjustable size.
    
    Args:
        image (np.ndarray): Input image
        points (np.ndarray): Points defining board corners
        scale (float): Scaling factor for expanding the board shape
    
    Returns:
        np.ndarray: Transformed board image
    """
    # Order points correctly
    rect = points.reshape(4, 2)

    # Compute the center of the quadrilateral
    center = np.mean(rect, axis=0)

    # Expand points outward while keeping the shape centered
    expanded_rect = center + (rect - center) * scale

    # Compute new width and height after expansion
    widthA = np.linalg.norm(expanded_rect[2] - expanded_rect[3])  # Bottom width
    widthB = np.linalg.norm(expanded_rect[1] - expanded_rect[0])  # Top width
    max_width = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(expanded_rect[1] - expanded_rect[2])  # Right height
    heightB = np.linalg.norm(expanded_rect[0] - expanded_rect[3])  # Left height
    max_height = max(int(heightA), int(heightB))

    # Define the destination points for perspective transformation
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")

    # Compute perspective transform matrix
    M = cv2.getPerspectiveTransform(expanded_rect, dst)
    warped = cv2.warpPerspective(image, M, (max_width, max_height))

    return warped


def detect_intersections( board_image):
    """
        Detect board intersections
        Args:
            board_image (np.ndarray): Transformed board image
        Returns:
            list: Intersection points
        """
    # Convert to grayscale
    gray = cv2.cvtColor(board_image, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Detect circles (potential intersections)
    circles = cv2.HoughCircles(
            edges, 
            cv2.HOUGH_GRADIENT, 
            dp=1, 
            minDist=20,
            param1=50, 
            param2=30, 
            minRadius=5, 
            maxRadius=20
        )
    
    # If circles found, return their centers
    if circles is not None:
            return circles[0, :, :2]
    return []

def detect_pieces( board_image):
    """
        Detect black and white pieces on the board
        Args:
            board_image (np.ndarray): Transformed board image
        Returns:
            tuple: (black_pieces, white_pieces)
        """
    # Convert to HSV for better color segmentation
    hsv = cv2.cvtColor(board_image, cv2.COLOR_BGR2HSV)
    
    # Define color ranges for black and white pieces
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])
    
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    
    # Create masks
    black_mask = cv2.inRange(hsv, lower_black, upper_black)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # Find contours for pieces
    black_contours, _ = cv2.findContours(
            black_mask, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
    white_contours, _ = cv2.findContours(
            white_mask, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
    
    # Filter contours by area to remove noise
    black_pieces = [
            cv2.minEnclosingCircle(cnt)[0] 
            for cnt in black_contours 
            if 10 < cv2.contourArea(cnt) < 100
        ]
    
    white_pieces = [
            cv2.minEnclosingCircle(cnt)[0] 
            for cnt in white_contours 
            if 10 < cv2.contourArea(cnt) < 100
        ]
    
    return black_pieces, white_pieces

def detect_board( image):
    """
        Main board detection method
        Args:
            image (np.ndarray): Input image
        Returns:
            dict: Detection results
        """
    # Preprocess image
    preprocessed = self.preprocess_image(image)
    
    # Find board contours
    board_candidates = self.find_board_contours(preprocessed)
    
    # If no board found, return None
    if not board_candidates:
            return None
    
    # Use the first (largest) board candidate
    board_points = board_candidates[0]
    
    # Apply perspective transform
    warped_board = self.perspective_transform(image, board_points)
    
    # Detect intersections
    intersections = self.detect_intersections(warped_board)
    
    # Detect pieces
    black_pieces, white_pieces = self.detect_pieces(warped_board)
    
    return {
            'board_points': board_points,
            'warped_board': warped_board,
            'intersections': intersections,
            'black_pieces': black_pieces,
            'white_pieces': white_pieces
        }

# Example usage
def main():
    # Load image
    image = cv2.imread('go_board.jpg')
    
    # Initialize detector
    detector = GoBoardDetector(debug=True)
    
    # Detect board
    result = detector.detect_board(image)
    
    if result:
        # Visualize results
        cv2.drawContours(image, [result['board_points']], -1, (0, 255, 0), 3)
        
        # Draw intersections
        for pt in result['intersections']:
            cv2.circle(result['warped_board'], tuple(map(int, pt)), 5, (0, 0, 255), -1)
        
        # Draw pieces
        for piece in result['black_pieces']:
            cv2.circle(result['warped_board'], tuple(map(int, piece)), 10, (0, 0, 0), -1)
        
        for piece in result['white_pieces']:
            cv2.circle(result['warped_board'], tuple(map(int, piece)), 10, (255, 255, 255), 2)
        
        # Show results
        cv2.imshow('Original with Board Contour', image)
        cv2.imshow('Warped Board', result['warped_board'])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys

    # Example usage:
    image = cv2.imread(sys.argv[1])

    # Preprocess image
    preprocessed = preprocess_image(image)
    
    # Find board contours
    board_candidates = find_board_contours(preprocessed)
    
    # If no board found, return None
    if not board_candidates:
        print('no candidates')
    
    # Use the first (largest) board candidate
    board_points = board_candidates[0]
    
    # Apply perspective transform
    warped_board = perspective_transform(image, board_points,scale=1.4)

    cv2.drawContours(image, [board_points], -1, (0, 255, 0), 3)
        
    # Show results
    cv2.imshow('Original with Board Contour', image)
    cv2.imshow('Warped Board', warped_board)
    cv2.waitKey(0)
    cv2.destroyAllWindows()