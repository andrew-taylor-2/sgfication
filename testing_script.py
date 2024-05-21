from sgfication import img_functions as im
import numpy as np

rowss,columnss=im.get_all_spacing(r"assets\board_shot.png")

black_matches = im.find_matches(r"assets\board_shot.png",r"C:\Users\andre\OneDrive\Pictures\Screenshots\assets\OGS_blackpiece_cropped.png")
intersection_matches = im.find_matches(r"assets\board_shot.png",r"C:\Users\andre\OneDrive\Pictures\Screenshots\assets\OGS_intersection_cropped.png")
white_matches = im.find_matches(r"assets\board_shot.png",r"C:\Users\andre\OneDrive\Pictures\Screenshots\assets\OGS_whitepiece_cropped.png")

allmatches=black_matches.copy() 
allmatches.extend(white_matches)
allmatches.extend(intersection_matches)

lowest_x,lowest_y = im.get_lowest_index(allmatches)

board_white,grid_white= im.consolidate_matches(white_matches,rowss,columnss,lowest_x,lowest_y)
board_black,grid_black= im.consolidate_matches(black_matches,rowss,columnss,lowest_x,lowest_y)
board_inter,grid_inter= im.consolidate_matches(intersection_matches,rowss,columnss,lowest_x,lowest_y)

bool_white=np.zeros((19,19),dtype=bool)
for x,y in board_white:
    bool_white[x,y]=True

bool_black=np.zeros((19,19),dtype=bool)
for x,y in board_black:
    bool_black[x,y]=True

bool_inter=np.zeros((19,19),dtype=bool)
for x,y in board_inter:
    bool_inter[x,y]=True

#import importlib
#importlib.reload(im)

### let's display some things
import matplotlib.pyplot as plt
import matplotlib.colors

# Assume bool_white, bool_black, and bool_empty are your boolean arrays
# First, initialize a 19x19 array filled with zeros (representing empty spaces)
board_representation = np.zeros((19, 19))

# Update the board representation with values for white and black pieces
# Assuming 1 for white pieces and 2 for black pieces
board_representation[bool_white] = 1
board_representation[bool_black] = 2

# flip x and y
board_representation = board_representation.T

# Define a custom colormap for the categories
# Here, 0: blue for empty, 1: white for white pieces, 2: black for black pieces
cmap = matplotlib.colors.ListedColormap(['blue', 'white', 'black'])
bounds = [0,1,2,3]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

# Plot the board
plt.figure(figsize=(8,8))
plt.imshow(board_representation, cmap=cmap, norm=norm)

# Optionally, add a grid
plt.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
plt.xticks(np.arange(-.5, 19, 1), [])
plt.yticks(np.arange(-.5, 19, 1), [])

# Adjust grid to fit the board
plt.xlim(-0.5, 18.5)
plt.ylim(18.5, -0.5)

plt.show()


### let's create some SGFs
sgfgame = im.create_sgf(bool_white, bool_black)
im.save_sgf(sgfgame,"../test3.sgf")