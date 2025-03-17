from os import listdir
from os.path import isfile, join, splitext, basename
import crop_piece
from pathlib import Path


def generate_new_file_path(original_path, appended='_cropped'):
    """Generates a new file path with string appended."""

    original_path = Path(original_path)
    new_file_name = f"{original_path.stem}{appended}{original_path.suffix}"
    return original_path.parent / new_file_name

if __name__ == "__main__":

    #give it a folder with piece, intersection screenshots. exclude file should be  a screenshot of the whole board.
    # it will spit out all the smaller screenshots cropped right

    crop_folder = Path(r"C:\Users\andre\OneDrive\Pictures\Screenshots\assets\OGS2")
    exclude_file = crop_folder / "OGS_board_2.png"

    # Get files in dir except exclude_file
    files = [f for f in crop_folder.iterdir() if f.is_file() and f != exclude_file]

    for f in files:
        new_full_path = generate_new_file_path(f)

        try:
            crop_piece.crop_piece(str(exclude_file), str(f), outfile=str(new_full_path))
        except Exception as e:  
            print(f"there was an error with file {f}: {e}")



