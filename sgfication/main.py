from fastapi import FastAPI, UploadFile, File, HTTPException
from img_functions import get_all_spacing
import numpy as np
import cv2 as cv

app = FastAPI()

@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):
    if file.content_type.startswith('image/'):
        # Read image file
        image_data = await file.read()
        image_array = np.fromstring(image_data, np.uint8)
        image = cv.imdecode(image_array, cv.IMREAD_COLOR)

        # Save temporary image to disk to use with the existing function
        temp_img_path = 'temp_image.jpg'
        cv.imwrite(temp_img_path, image)

        # Call the function from img_functions.py
        row_spacing, column_spacing = get_all_spacing(temp_img_path)
        return {"row_spacing": row_spacing, "column_spacing": column_spacing}
    else:
        raise HTTPException(status_code=400, detail="File provided is not an image.")

