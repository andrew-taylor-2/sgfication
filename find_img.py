import argparse
import numpy as np
from scipy.signal import convolve2d
from PIL import Image

def find_best_match_location(large_image_path, small_image_paths):
    # load the large image and convert it to grayscale
    large_image = Image.open(large_image_path).convert('L')
    large_image_np = np.asarray(large_image)
    
    # initialize variables to keep track of the best match
    best_match_value = -np.inf
    best_match_location = None
    best_match_index = None
    
    for i, small_image_path in enumerate(small_image_paths):
        # load the small image, convert it to grayscale. convert to desired dtype of convolution output
        small_image = Image.open(small_image_path).convert('L')
        small_image_np = np.asarray(small_image).astype(np.float32)
        
        # perform 2D convolution (flip kernel)
        result = convolve2d(large_image_np, small_image_np[::-1,::-1], mode='valid')
        
        # find the peak value in the convolution result
        max_value = np.max(result)
        
        # check if this result is better than what we've seen before
        if max_value > best_match_value:
            best_match_value = max_value
            y, x = np.unravel_index(np.argmax(result), result.shape)
            best_match_location = (x, y)
            best_match_index = i
    
    # return the index of the best matching small image and its location
    return best_match_index, best_match_location

# if called from terminal
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find which of the smaller images is contained in the larger image and its location.')
    parser.add_argument('large_image_path', type=str, help='Path to the large image')
    parser.add_argument('small_image_paths', type=str, nargs='+', help='Path to the small images')

    args = parser.parse_args()

    best_match_index, location = find_best_match_location(args.large_image_path, args.small_image_paths)
    print(f"Small image {best_match_index} is the best match, located at: {location}")