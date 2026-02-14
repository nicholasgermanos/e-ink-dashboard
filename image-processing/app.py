# Source - https://stackoverflow.com/a
# Posted by lizisong1988, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-01, License - CC BY-SA 4.0

import base64
import time
from io import BytesIO

import cv2
from flask import Flask
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DISPLAY_HEIGHT = 984
DISPLAY_WIDTH = 1304

MAX_CHUNK_SIZE = DISPLAY_HEIGHT * DISPLAY_WIDTH / 64
CHROME_SCREENSHOT_SCALE = 3

def screenshot():

    chrome_options = Options()
    chrome_options = webdriver.ChromeOptions();

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument('--font-render-hinting=none')
    chrome_options.add_argument('--disable-font-subpixel-positioning')
    chrome_options.add_argument('--disable-lcd-text')
    chrome_options.add_argument("--force-device-scale-factor=3")
    chrome_options.add_argument("--high-dpi-support=1")
    chrome_options.add_argument("--force-color-profile=srgb")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(DISPLAY_HEIGHT, DISPLAY_WIDTH)
    driver.get("http://127.0.0.1:8000/")

    screenshot = driver.execute_cdp_cmd(
        "Page.captureScreenshot",
        {
            "captureBeyondViewport": True,
            "fromSurface": True,
            "format": "png",
            "optimizeForSpeed": False,
        },
    )

    time.sleep(2)

    img_data = base64.b64decode(screenshot["data"])
    img = Image.open(BytesIO(img_data))
    img = img.resize((img.width // CHROME_SCREENSHOT_SCALE, img.height //  CHROME_SCREENSHOT_SCALE), Image.NEAREST)

    img.save("screenshot.png")

    driver.quit()


def convert_greyscale():
    img = Image.open("screenshot.png")
    out = Image.new("I", img.size, 0xFFFFFF)

    width, height = img.size

    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            if r == b == g and r < 195:
                out.putpixel((x, y), 0)

    out.save("xscale.png")
    # subprocess.run(["magick", "red.jpg", "-remap", "palette.gif", "dithered.png"])


def convert_redscale():
    img = Image.open("screenshot.png")
    out = Image.new("I", img.size, 0xFFFFFF)

    width, height = img.size

    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            if r > 200 and g < 230 and b < 230 and not (r == b == g):
                out.putpixel((x, y), 0)

    out.save("xscale.png")


def convert_binary():

    # read the image file
    img = cv2.imread("xscale.png", 0)

    height, width = img.shape

    ret, bw_img = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY)

    # converting to its binary form
    bw = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY)

    # print(type(bw[1]))
    with open("output.txt", "r+") as file:
        file.truncate(0)
        for x in bw[1]:
            for y in x:
                raw = int(y)
                out = 1 if raw == 255 else 0
                file.write(f"{out}")
    #
    # cv2.imshow("Binary", bw_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return width


app = Flask(__name__)


@app.route("/generate")
def generate():
    screenshot()
    convert_greyscale()
    return str(convert_binary())


@app.route("/generatered")
def generatered():
    convert_redscale()
    return str(convert_binary())


@app.route("/0")
def fetch_0():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 0
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/1")
def fetch_1():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 1
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/2")
def fetch_2():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 2
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/3")
def fetch_3():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 3
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/4")
def fetch_4():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 4
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/5")
def fetch_5():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 5
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/6")
def fetch_6():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 6
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/7")
def fetch_7():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 7
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/8")
def fetch_8():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 8
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/9")
def fetch_9():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 9
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/10")
def fetch_10():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 10
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/11")
def fetch_11():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 11
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/12")
def fetch_12():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 12
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/13")
def fetch_13():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 13
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/14")
def fetch_14():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 14
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/15")
def fetch_15():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 15
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/16")
def fetch_16():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 16
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/17")
def fetch_17():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 17
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/18")
def fetch_18():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 18
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/19")
def fetch_19():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 19
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/20")
def fetch_20():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 20
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/21")
def fetch_21():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 21
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/22")
def fetch_22():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 22
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/23")
def fetch_23():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 23
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/24")
def fetch_24():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 24
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/25")
def fetch_25():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 25
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/26")
def fetch_26():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 26
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/27")
def fetch_27():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 27
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/28")
def fetch_28():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 28
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/29")
def fetch_29():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 29
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/30")
def fetch_30():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 30
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/31")
def fetch_31():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 31
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/32")
def fetch_32():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 32
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/33")
def fetch_33():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 33
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/34")
def fetch_34():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 34
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/35")
def fetch_35():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 35
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/36")
def fetch_36():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 36
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/37")
def fetch_37():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 37
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/38")
def fetch_38():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 38
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/39")
def fetch_39():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 39
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/40")
def fetch_40():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 40
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/41")
def fetch_41():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 41
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/42")
def fetch_42():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 42
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/43")
def fetch_43():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 43
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/44")
def fetch_44():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 44
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/45")
def fetch_45():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 45
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/46")
def fetch_46():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 46
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/47")
def fetch_47():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 47
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/48")
def fetch_48():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 48
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/49")
def fetch_49():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 49
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/50")
def fetch_50():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 50
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/51")
def fetch_51():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 51
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/52")
def fetch_52():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 52
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/53")
def fetch_53():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 53
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/54")
def fetch_54():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 54
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/55")
def fetch_55():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 55
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/56")
def fetch_56():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 56
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/57")
def fetch_57():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 57
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/58")
def fetch_58():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 58
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/59")
def fetch_59():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 59
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/60")
def fetch_60():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 60
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/61")
def fetch_61():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 61
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/62")
def fetch_62():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 62
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]


@app.route("/63")
def fetch_63():
    file = open("output.txt", "r")
    content = file.read()
    start_index = MAX_CHUNK_SIZE * 63
    end_index = start_index + MAX_CHUNK_SIZE
    return content[int(start_index) : int(end_index)]
