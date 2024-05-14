import requests

url = 'http://localhost:8000/upload'
files = {'image': open('/path/to/your/image.jpg', 'rb')}

response = requests.post(url, files=files)
print(response.text)
