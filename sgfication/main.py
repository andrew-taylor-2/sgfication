from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sgfication.img_functions import get_all_spacing, find_matches, get_lowest_index, consolidate_matches, create_sgf
import numpy as np
import cv2 as cv
#db stuff
import asyncpg
import os
from dotenv import load_dotenv


app = FastAPI()

@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):
    if file.content_type.startswith('image/'):
        # Read image file
        image_data = await file.read()
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv.imdecode(image_array, cv.IMREAD_GRAYSCALE)

        # Call the function from img_functions.py
        row_spacing, column_spacing = get_all_spacing(image)

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

        bool_white=np.zeros((19,19),dtype=bool)
        for x,y in board_white:
            bool_white[x,y]=True

        bool_black=np.zeros((19,19),dtype=bool)
        for x,y in board_black:
            bool_black[x,y]=True

        #rotate render by 90 degrees here
        bool_white = np.rot90(bool_white)
        bool_black = np.rot90(bool_black)
        sgfgame = create_sgf(bool_white, bool_black)
        sgf_data = sgfgame.serialise().decode('utf-8')
        print(sgf_data)

        #send to db
        await save_to_db(file.filename, sgf_data)

        return JSONResponse(content={"sgf": sgf_data})

    else:
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    

async def save_to_db(filename: str, sgf_data: str):
    load_dotenv('sgfication/pg.env') #why do i have to give folder ?
    print(os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_NAME'), os.getenv('DB_HOST'))
    conn = await asyncpg.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                                 database=os.getenv('DB_NAME'), host=os.getenv('DB_HOST'))
    await conn.execute('''
        INSERT INTO submissions(file_name, sgf_data) 
        VALUES($1, $2)
    ''', filename, sgf_data)
    await conn.close()
    

# Add CORS middleware
load_dotenv('url.env')
allowed_origins = os.getenv('FRONTEND_ADDRESS',"").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins if origin],  # frontend location
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
