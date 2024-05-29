# SGFication: Go Board Identification 

## Overview
SGFication is an app that takes Go board screenshots and places the detected position on an interactable board using computer vision tools.

## Components
- **Board Recognition**: Uses computer vision to identify the state of the Go board from images.
- **React Frontend**: Takes user uploaded images and renders the board state, allowing for interaction.
- **API Backend**: Receives uploads via HTTP to a Uvicorn ASGI server which runs the CV app and sends results to the frontend

## Tech Stack
- **Python**: Used for the backend and computer vision components, as well as FastAPI for interaction with frontend.
- **OpenCV**: Used for image processing and computer vision tasks.
- **JavaScript/React/CSS**: Frontend interaction and visualization.
- **Node.js**: Server-side runtime environment to handle web server logic.
- **WGO.js**: JavaScript library used for board display and interaction on the web frontend. Their code [here](https://github.com/waltheri/wgo.js/)

## Setup Instructions

1. **Clone the Repository**: `git clone https://github.com/yourusername/sgfication.git`
2. **Backend Setup**:
   - Create and activate the Conda environment: `conda env create -f environment.yml && conda activate sgfenv`
   - Start the server: `conda run --no-capture-output -n sgfenv uvicorn sgfication.main:app --host 0.0.0.0 --port 8000`
3. **Frontend Setup**:
   - Navigate to the frontend directory: `cd frontend/sgf-app`
   - Install dependencies: `npm install`
   - Start the frontend server: `npm run dev`