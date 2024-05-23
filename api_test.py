import requests
#
# The URL of the FastAPI server endpoint
url = 'http://127.0.0.1:5000/analyze/'
#
# Path to the image file you want to analyze
image_path = r'C:\Users\andre\Software\Repos\sgfication\assets\board_shot.png'
#
# Open the image file in binary mode
with open(image_path, 'rb') as image_file:
    #
    # Define the file payload as a dictionary
    files = {'file': (image_path, image_file, 'image/png')}
    # Send the POST request
    response = requests.post(url, files=files)
    # Print the response from the server
    print(response.text)


    
# potential upload POST request?
# url = 'http://localhost:8000/upload'
# files = {'image': open('/path/to/your/image.jpg', 'rb')}

# response = requests.post(url, files=files)
# print(response.text)

# ["conda", "run", "--no-capture-output", "-n", "sgfenv", "uvicorn", "sgfication.main:app", "--host", "0.0.0.0", "--port", "8000"]
