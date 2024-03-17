from os import listdir
from os.path import isfile, join, splitext, basename
import crop_piece

crop_folder = r"C:\Users\andre\OneDrive\Pictures\Screenshots\assets"
exclude = r"C:\Users\andre\OneDrive\Pictures\Screenshots\assets\OGS_default_board.png"
board = exclude

#get files in dir
files = [f for f in listdir(crop_folder) if isfile(join(crop_folder, f)) and join(crop_folder, f) != exclude]

for f in files:
    # Generate the new file name with '_cropped' appended before the file extension
    full_path = join(crop_folder, f)  # Get the full path of the file
    file_name_without_ext, file_ext = splitext(basename(full_path))  # Split the basename and extension
    new_file_name = f"{file_name_without_ext}_cropped{file_ext}"  # Append '_cropped' to the file name
    new_full_path = join(crop_folder, new_file_name)  # Generate the new full path

    # Use the new_full_path as the outfile parameter
    try:
        crop_piece.crop_piece(board, full_path, outfile=new_full_path)

    except:
        print(f"there was an error with file {full_path}")

