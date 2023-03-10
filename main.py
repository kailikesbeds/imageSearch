from flask import Flask, request
import PIL
from PIL import Image
import requests
from bs4 import BeautifulSoup
from io import BytesIO

def search_images(query):
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")
    return images


app = Flask(__name__)

@app.route('/search', methods=['POST'])
def receive():
    response = request.get_json()
    word = response['key']

    imgUrl = search_images(word)[1]["src"]
    if imgUrl:
      with requests.get(imgUrl) as response:
        img = Image.open(BytesIO(response.content))

    everything = []
    sizeX, sizeY = img.size

    for row in range(0, sizeY):
        line = []
        for pixel in range(0, sizeX):
            try:
                line.append(img.getpixel((pixel, row)))
            except:
                pass

        if not line:
            pass
        else:
            everything.append(line)
    
    return [img.size[0],img.size[1],everything]


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)