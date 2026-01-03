# Source - https://stackoverflow.com/a
# Posted by lizisong1988, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-01, License - CC BY-SA 4.0

# coding=utf-8
from flask import Flask
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import cv2

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def screenshot():
    # please note that we MUST use headless mode
    # 1304*984
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://cdn.britannica.com/33/155133-050-962670B6/Sydney-Harbour-Bridge-Australia-Syndey.jpg")
    time.sleep(2)

    # height = 984 / 2
    height = 200
    # width = 1304 / 2
    width = 255
    driver.set_window_size(width, height)

    time.sleep(2)
    driver.save_screenshot("screenshot.png")
    driver.quit()

def convert_greyscale():
    img = Image.open('img.png').convert('L')
    img.save('greyscale.png')

def convert_binary():

    # read the image file
    img = cv2.imread('greyscale.png', 2)

    ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # converting to its binary form
    bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)


    print(len(bw[1]))
    # print(type(bw[1]))
    bw[1].tofile("output.txt")
    with open("output.txt", "r+") as file:
        file.truncate(0)
        for x in bw[1]:
            for y in x:
                raw = int(y)
                out = 1 if raw == 255 else 0
                file.write(f"{out}")

    cv2.imshow("Binary", bw_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#
# if __name__ == "__main__":
#     screenshot()
#     convert_greyscale()
#     convert_binary()
