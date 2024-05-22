from fastapi import FastAPI, UploadFile, File, HTTPException
from sgfication.img_functions import get_all_spacing, find_matches, get_lowest_index, consolidate_matches, create_sgf
import numpy as np
import cv2 as cv

app = FastAPI()

@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):
    if file.content_type.startswith('image/'):
        # Read image file
        image_data = await file.read()
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv.imdecode(image_array, cv.IMREAD_GRAYSCALE)
        # Save temporary image to disk to use with the existing function
        #temp_img_path = 'temp_image.jpg'
        #cv.imwrite(temp_img_path, image)
        # Call the function from img_functions.py
        row_spacing, column_spacing = get_all_spacing(image)
        
        #return {"row_spacing": row_spacing, "column_spacing": column_spacing}

        # in app
        #black_matches = find_matches(image, "/app/assets/ogs/OGS_blackpiece_cropped.png")
        #intersection_matches = find_matches(image, "/app/assets/ogs/OGS_intersection_cropped.png")
        #white_matches = find_matches(image, "/app/assets/ogs/OGS_whitepiece_cropped.png")

        # not in app
        black_matches = find_matches(image, "assets/ogs/OGS_blackpiece_cropped.png",visualize=False)
        intersection_matches = find_matches(image, "assets/ogs/OGS_intersection_cropped.png",visualize=False)
        white_matches = find_matches(image, "assets/ogs/OGS_whitepiece_cropped.png",visualize=False)

        allmatches=black_matches.copy() 
        allmatches.extend(white_matches)
        allmatches.extend(intersection_matches)

        lowest_x,lowest_y = get_lowest_index(allmatches)

        board_white, _= consolidate_matches(white_matches,row_spacing,column_spacing,lowest_x,lowest_y)
        board_black, _= consolidate_matches(black_matches,row_spacing,column_spacing,lowest_x,lowest_y)
        #board_inter, _= consolidate_matches(intersection_matches,row_spacing,column_spacing,lowest_x,lowest_y)

        bool_white=np.zeros((19,19),dtype=bool)
        for x,y in board_white:
            bool_white[x,y]=True

        bool_black=np.zeros((19,19),dtype=bool)
        for x,y in board_black:
            bool_black[x,y]=True

        #bool_inter=np.zeros((19,19),dtype=bool)
        #for x,y in board_inter:
        #    bool_inter[x,y]=True

        sgfgame = create_sgf(bool_white, bool_black)
        print(sgfgame.serialise().decode('utf-8'))

    else:
        raise HTTPException(status_code=400, detail="File provided is not an image.")
